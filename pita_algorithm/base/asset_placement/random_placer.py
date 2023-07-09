import random
import numpy as np
import webcolors
from typing import Callable, Union, Any
from PIL import ImageColor
from random import sample
from pita_algorithm.base.asset_placement.validator import Validator
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from pita_algorithm.base.asset_placement.abstract_placer import AbstractPlacer


class PlacerDistribution:
    """Abstract class for Placers Distributions."""

    def __init__(self, distribution: Callable, *args: Any):
        """Constructor for distributions used in the RandomPlacer. The distribution
        object will be called with *args as parameters.
        Write for instance:
        `PlacerDistribution(np.random.default_rng().normal, 2, 1)` if you intend
        to sample from a normal distribution with loc=2 and scale = 1
        The samples will be drawn independently, which results in square like shapes.

        Parameters:
            distribution (Callable): Distribution(*args) will be used for sampling values
            *args (Any): Parameters for the random distribution
        """
        self.distribution = distribution
        self.parameters = args

    def __call__(self) -> tuple[float, float]:
        """Draws a sample from the distribution.

        Returns:
            (tuple[float, float]): Sampled x and y coordinates
        """
        return self.distribution(*self.parameters), self.distribution(*self.parameters)


class Placer2DDistribution(PlacerDistribution):
    """Class for two dimensional distributions, otherwise equivalent to its parent class."""

    def __call__(self) -> tuple[float, float]:
        """Draws a sample from the distribution

        Returns:
            (float, float): Sampled x and y coordinates
        """
        x, y = self.distribution(*self.parameters)
        return (x, y)


class CircularUniformDistribution(PlacerDistribution):
    """Class for holing Distribution with specific parameterizations."""

    def __init__(self, loc: float = 0, scale: float = 10.0):
        """Distribution for uniformly drawing samples from a circle.

        Parameters:
            loc (float): Minimal euclidean distance from the center
            scale (float): Maximal euclidean distance from the center
        """
        self.loc = loc
        self.scale = scale

    def __call__(self):
        """Draws a sample from the distribution.

        Returns:
            (float, float): Sampled x and y coordinates
        """
        length = np.sqrt(np.random.uniform(self.loc, self.scale**2))
        angle = np.pi * np.random.uniform(0, 2)

        x = length * np.cos(angle)
        y = length * np.sin(angle)
        return x, y


class RandomPlacer(AbstractPlacer):
    """Places objects in a random manner."""

    # The validator does not check, if the addition of an item is possible.
    # Instead, after placement has failed for MAX_TRIES times, an error is thrown.
    MAX_TRIES = 10000

    def __init__(self, distribution: PlacerDistribution):
        """Constructor of the RandomPlacer class.

        Parameters:
            distribution (PlacerDistribution): Distribution used for sampling
        """
        self.distribution = distribution

    def add(
        self,
        site: AbstractSite,
        mujoco_object_blueprint: MujocoObject,
        mujoco_object_rule_blueprint: MujocoObject,
        validators: list[Validator],
        amount: tuple[int, int] = (1, 1),
        z_rotation_range: Union[tuple[int, int], None] = None,
        color_groups: Union[tuple[int, int], None] = None,
        size_groups: Union[tuple[int, int], None] = None,
        size_value_range: Union[tuple[int, int], None] = None
    ):
        """Adds a mujoco object to a site by calling the sites add method
        after checking placement via the validator.

        Parameters:
            site (AbstractSite): Site class instance where the object is added to
            mujoco_object_blueprint (MujocoObject): To-be-placed mujoco object
            mujoco_object_rule_blueprint (MujocoObject): Blueprint of the to-be-placed mujoco object
            validators (list[Validator]): List of validators used to check object placement
            amount (tuple[int, int]): Range of possible amount of objects to be placed
            z_rotation_range (Union[tuple[int, int]]): Range of degrees for z-axis rotation
            color_groups (Union[tuple[int, int], None]): Range of possible different colors for object
            size_groups (Union[tuple[int, int], None]): Range of possible different sizes for object
            size_value_range (Union[tuple[float, float]]): Range of size values allowed in randomization
        """

        # sample from amount range
        amount = self._sample_from_amount(amount=amount)

        # get colors rgba
        if not color_groups is None:
            if max(color_groups) > amount:
                raise ValueError("Not enough objects for specified colors.")
        colors_for_placement = self._get_random_colors(amount=amount, color_groups=color_groups)

        # get object size
        if not size_groups is None:
            if len(size_groups) > amount:
                raise ValueError("Not enough objects for specified sizes.")
        sizes_for_placement = self._get_random_sizes(amount=amount, size_groups=size_groups,
                                                     size_value_range=size_value_range)

        for i in range(amount):
            if not colors_for_placement is None:
                # apply colors to objects
                mujoco_object_rule_blueprint.color = colors_for_placement[i]

            if not sizes_for_placement is None:
                # apply sizes to objects
                mujoco_object_rule_blueprint.size = sizes_for_placement[i]

            # Save size of object for setting the z coordinate
            new_z_position = mujoco_object_rule_blueprint.size[0]

            # Sample a new position
            mujoco_object_rule_blueprint.position = (
                *self.distribution(),
                new_z_position,
            )

            count = 0
            # Ask every validator for approval until all approve or MAX_TRIES is reached,
            # then throw error
            while not all(
                [
                    validator.validate(
                        mujoco_object=mujoco_object_rule_blueprint, site=site
                    )
                    for validator in validators
                ]
            ):
                count += 1
                if count >= RandomPlacer.MAX_TRIES:
                    raise RuntimeError(
                        "Placement of object '{}' in site '{}' has failed '{}' times, please check your config.yaml".format(
                            mujoco_object_blueprint.name,
                            site.name,
                            RandomPlacer.MAX_TRIES,
                        )
                    )
                # If placement is not possible, sample a new position
                mujoco_object_rule_blueprint.position = (
                    *self.distribution(),
                    new_z_position,
                )

            # Copy the blueprint to avoid changing the original
            mujoco_object = self._copy(mujoco_object_blueprint)

            if colors_for_placement is not None:
                # Exchange parameters i.e. Reset rule blueprint and modify the mujoco_object copy
                old_color = mujoco_object.color
                mujoco_object.color = mujoco_object_rule_blueprint.color
                mujoco_object_rule_blueprint.color = old_color

            if sizes_for_placement is not None:
                # Exchange parameters i.e. Reset rule blueprint and modify the mujoco_object copy
                old_size = mujoco_object.size
                mujoco_object.size = mujoco_object_rule_blueprint.size
                mujoco_object_rule_blueprint.size = old_size

            mujoco_object.position = mujoco_object_rule_blueprint.position

            # Keep track of the placement in the validators
            for validator in validators:
                validator.add(mujoco_object)

            # Add the object to the site
            site.add(mujoco_object=mujoco_object)

    def remove(self, site: AbstractSite, mujoco_object: MujocoObject):
        """Removes a mujoco object from a site by calling the sites remove method.

        Parameters:
            site (AbstractSite): Site class instance where the object is removed from
            mujoco_object (MujocoObject): To-be-removed mujoco object
        """
        site.remove(mujoco_object=mujoco_object)

    @staticmethod
    def _sample_from_amount(amount: tuple[int, int]) -> int:
        """Sample the amount of objects to be placed if amount is a tuple and differ

        Parameters:
            amount (tuple[int, int]): Range of number of objects for randomization

        Returns:
            amount_int (int): Random number of amount picked in given range
        """
        amount_int = (
            amount[0]
            if (amount[0] == amount[1])
            else np.random.randint(int(amount[0]), int(amount[1]) + 1)  # randint function is exclusive on high val
        )
        return amount_int

    def _get_random_colors(self, amount: int,
        color_groups: Union[tuple[int, int], None]
    ) -> Union[list[list[float]], None]:
        """Returns a list of random rgba colors (with alpha=1).
           Every color is added twice to the list.

        Parameters:
            amount (Union[tuple[int, int], None): Range of amount of object
            color_groups (Union[tuple[int, int], None]): Range of different colors

        Returns:
            colors_rgba (Union[list[list[float]], None]): List of randomized rgba colors
        """
        if color_groups is None:
            return None

        # get list of available color names
        color_names = list(webcolors.CSS3_NAMES_TO_HEX.keys())

        # get random int in range of colors
        colors_randint = (
            color_groups[0]
            if (color_groups[0] == color_groups[1])
            else np.random.randint(int(color_groups[0]), int(color_groups[1]) + 1)  # higher is excluding
        )

        # get number of different colors needed by amount / color_groups
        colors_needed = int(amount / colors_randint)    # int type cast automatically rounds down

        # get random rgba for number of colors needed
        colors_rgba = list()
        colors_used = list()
        for _ in range(colors_needed):
            rand_color_int = np.random.randint(0, len(color_names) + 1)
            random_color = color_names[rand_color_int]
            while random_color in colors_used:
                random_color = color_names[rand_color_int]
            colors_used.append(random_color)
            color_rgba = self._get_rgba_from_color_name(random_color)
            color_rgba_normalized = [(float(val) / 255) for val in color_rgba]
            colors_rgba.append(color_rgba_normalized)

        # generate list of colors depending on amount an
        colors_for_placement = list()
        for color in colors_rgba:
            for _ in range(colors_randint):
                colors_for_placement.append(color)

        # fill colors_for_placement list if amount of objects is greater than colors in the list.
        # this happens if amount % color_groups != 0
        while amount > len(colors_for_placement):
            sampled_color = sample(colors_rgba, 1)[0]
            colors_for_placement.append(sampled_color)

        return colors_for_placement

    def _get_random_sizes(self, amount: int,
                          size_groups: Union[tuple[float, float], None],
                          size_value_range: Union[tuple[float, float], None]
                          ) -> Union[list[list[float]], None]:
        """Returns a list of random sizes. Every size is added twice to the list.

        Parameters:
            amount (int): Number of object
            size_groups (Union[tuple[float, float], None]): Range of different sizes
            size_value_range (Union[tuple[float, float], None]): Defines the value size of the randomization process

        Returns:
            sizes_for_placement (list(float)): List of randomized sizes
        """
        if size_groups is None:
            return None

        # get random int in range of sizes
        sizes_randint = (
            size_groups[0]
            if (size_groups[0] == size_groups[1])
            else np.random.randint(int(size_groups[0]), int(size_groups[1]) + 1)  # higher is excluding
        )

        ## get number of different sizes needed by amount / size_groups
        sizes_needed = int(amount / sizes_randint)    # int type cast automatically rounds down

        # get random sizes for number of sizes needed
        sizes = list()
        sizes_used = list()
        for _ in range(sizes_needed):
            random_size = self._get_size_array(size_value_range=size_value_range)
            while random_size in sizes_used:
                random_size = self._get_size_array(size_value_range=size_value_range)
            sizes_used.append(random_size)
            sizes.append(random_size)

        # generate list of colors depending on amount an
        sizes_for_placement = list()
        for size in sizes:
            for _ in range(sizes_randint):
                sizes_for_placement.append(size)

        # fill colors_for_placement list if amount of objects is greater than colors in the list.
        # this happens if amount % color_groups != 0
        while amount > len(sizes_for_placement):
            sampled_color = sample(sizes, 1)[0]
            sizes_for_placement.append(sampled_color)

        # apply shuffling so that color and size is not synchronized
        random.shuffle(sizes_for_placement)

        return sizes_for_placement

    def _get_rgba_from_color_name(self, color_name: str) -> Union[tuple[float, float, float, float], None]:
        """Takes color as argument and returns the corresponding rgba color code

        Parameters:
            color_name (str): Name of color

        Returns:
            rgba (Union[tuple[float, float, float, float]]): Tuple of rgba values for the corresponding color string
        """
        try:
            # Get hexadecimal color code
            hex_code = webcolors.name_to_hex(color_name)
            # Convert hexadecimal to RGBA
            rgba = ImageColor.getcolor(hex_code, "RGBA")
            return rgba
        except ValueError:
            # Handle invalid color names
            return None

    def _get_size_array(self, size_value_range: Union[tuple[float, float]]) -> Union[list[float, float, float]]:
        """Generates 3D random size in given range

        Parameters:
            size_value_range (Union[tuple[float, float]]): Range of possible size values

        Returns:
            random_size (Union[list[float, float, float]]): Randomized size values in given range for 3D
        """
        x_rand_size_float = np.random.uniform(size_value_range[0], size_value_range[1])  # higher is excluding
        y_rand_size_float = np.random.uniform(size_value_range[0], size_value_range[1])  # higher is excluding
        z_rand_size_float = np.random.uniform(size_value_range[0], size_value_range[1])  # higher is excluding
        random_size = [x_rand_size_float, y_rand_size_float, z_rand_size_float]
        return random_size
