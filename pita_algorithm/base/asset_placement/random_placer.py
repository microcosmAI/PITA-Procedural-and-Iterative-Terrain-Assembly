import random
import numpy as np
import webcolors
from typing import Callable, Union, Any
from PIL import ImageColor

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
            colors_range (Union[tuple[int, int], None]): Range of possible different colors for object
            sizes_range (Union[tuple[int, int], None]): Range of possible different sizes for object
        """

        # sample from amount range
        amount = self._sample_from_amount(amount=amount)

        # get colors rgba
        colors_rgba = self._get_random_colors(amount=amount, color_groups=color_groups)
        ############################################################### Move to function
        # ToDo: check since it actually currently gets a list of double the amount
        if not colors_rgba is None:
            if len(colors_rgba) > amount:
                raise ValueError("Not enough objects for specified colors.")

        # get object size
        # ToDo: check since it actually currently gets a list of double the amount
        sizes = self._get_random_sizes(sizes_range=size_groups)
        if not sizes is None:
            if len(sizes) > amount:
                raise ValueError("Not enough objects for specified sizes.")
        ###############################################################

        # ToDo: adjust
        for i in range(amount):
            if not colors_rgba is None:
                # apply colors to objects
                if i > (len(colors_rgba) - 1):
                    randint = random.randrange(len(colors_rgba))
                    mujoco_object_rule_blueprint.color = colors_rgba[randint]
                else:
                    mujoco_object_rule_blueprint.color = colors_rgba[i]

            if not sizes is None:
                # apply sizes to objects
                if i > (len(sizes) - 1):
                    randint = random.randrange(len(sizes))
                    mujoco_object_rule_blueprint.size = sizes[randint]
                else:
                    mujoco_object_rule_blueprint.size = sizes[i]

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

            if colors_rgba is not None:
                # Exchange parameters i.e. Reset rule blueprint and modify the mujoco_object copy
                old_color = mujoco_object.color
                mujoco_object.color = mujoco_object_rule_blueprint.color
                mujoco_object_rule_blueprint.color = old_color

            if sizes is not None:
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
        # Sample the amount of objects to be placed if amount is a tuple and differ
        amount = (
            amount[0]
            if (amount[0] == amount[1])
            else np.random.randint(int(amount[0]), int(amount[1]) + 1)  # randint function is exclusive on high val
        )
        return amount

    def _get_random_colors(self, amount: int,
        color_groups: Union[tuple[int, int], None]
    ) -> Union[list[tuple[float, float, float, float]], None]:
        """Returns a list of random rgba colors (with alpha=1).
           Every color is added twice to the list.

        Parameters:
            amount (Union[tuple[int, int], None): Range of amount of object
            color_groups (Union[tuple[int, int], None]): Range of different colors

        Returns:
            colors_rgba (Union[list[tuple[float, float, float, float]], None]): List of randomized rgba colors
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

        return colors_rgba

    @staticmethod
    def _get_random_sizes(
        sizes_range: Union[tuple[float, float], None]
    ) -> Union[list[list[float]], None]:
        """Returns a list of random sizes. Every size is added twice to the list.

        Parameters:
            sizes_range (Union[tuple[float, float], None]): Range of different sizes

        Returns:
            sizes (list(float)): List of randomized sizes between 0 and 2
        """
        if sizes_range is None:
            return None

        # get random int in range of colors
        sizes_randint = (
            sizes_range[0]
            if (sizes_range[0] == sizes_range[1])
            else np.random.randint(int(sizes_range[0]), int(sizes_range[1]))
        )

        # get random size for every size that exist
        sizes = list()
        for _ in range(sizes_randint):
            random_size = round(
                np.random.random() * 2, 2
            )  # sets a size between 0 and 2
            sizes.append([random_size])
            sizes.append([random_size])

        return sizes

    def _get_rgba_from_color_name(self, color_name):
        try:
            # Get hexadecimal color code
            hex_code = webcolors.name_to_hex(color_name)
            # Convert hexadecimal to RGBA
            rgba = ImageColor.getcolor(hex_code, "RGBA")
            return rgba
        except ValueError:
            # Handle invalid color names
            return None
