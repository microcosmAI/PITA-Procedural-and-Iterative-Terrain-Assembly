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
from pita_algorithm.base.asset_placement.abstract_placer_distribution import (
    AbstractPlacerDistribution,
)
from pita_algorithm.base.world_sites.area import Area
from pita_algorithm.base.world_sites.environment import Environment
from pita_algorithm.utils.general_utils import Utils


class RandomPlacer(AbstractPlacer):
    """Places objects in a random manner."""

    # The validator does not check, if the addition of an item is possible.
    # Instead, after placement has failed for MAX_TRIES times, an error is thrown.
    MAX_TRIES = 10000

    def __init__(self, distribution: AbstractPlacerDistribution):
        """Constructor of the RandomPlacer class.

        Parameters:
            distribution (AbstractPlacerDistribution): Distribution used for sampling
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
        size_value_range: Union[tuple[int, int], None] = None,
    ):
        """Adds a mujoco object to a site by calling the sites add method
        after checking placement via the validator.

        Parameters:
            site (AbstractSite): Site class instance where the object is added to
            mujoco_object_blueprint (MujocoObject): To-be-placed mujoco object
            mujoco_object_rule_blueprint (MujocoObject): Blueprint of the to-be-placed mujoco object
            validators (list[Validator]): List of validators used to check object placement
            amount (tuple[int, int]): Range of possible amount of objects to be placed
            z_rotation_range (Union[tuple[int, int], None]): Range of degrees for z-axis rotation
            color_groups (Union[tuple[int, int], None]): Range of possible different colors for object
            size_groups (Union[tuple[int, int], None]): Range of possible different sizes for object
            size_value_range (Union[tuple[float, float], None]): Range of size values allowed in randomization
        """

        # Sample from amount range
        amount: int = self._sample_from_amount(amount=amount)

        # Get colors rgba
        if not color_groups is None:
            if max(color_groups) > amount:
                raise ValueError("Not enough objects for specified colors.")
        colors_for_placement = self._get_random_colors(
            amount=amount, color_groups=color_groups
        )

        # Get object size
        if not size_groups is None:
            if len(size_groups) > amount:
                raise ValueError("Not enough objects for specified sizes.")
        sizes_for_placement = self._get_random_sizes(
            amount=amount, size_groups=size_groups, size_value_range=size_value_range
        )

        # Get object z-axis rotation
        z_rotation_for_placement = self._get_random_rotation(
            amount=amount, z_rotation_range=z_rotation_range
        )

        for i in range(amount):
            if not colors_for_placement is None:
                # Apply colors to objects
                mujoco_object_rule_blueprint.color = colors_for_placement[i]

            if not sizes_for_placement is None:
                # Apply sizes to objects
                mujoco_object_rule_blueprint.size = sizes_for_placement[i]

            if not z_rotation_for_placement is None:
                # Apply rotation to z-axis of object
                rotation = mujoco_object_rule_blueprint.rotation
                if rotation is None:
                    rotation = [0, 0, z_rotation_for_placement[i]]
                else:
                    rotation[2] = z_rotation_for_placement[i]
                mujoco_object_rule_blueprint.rotation = rotation

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

            if z_rotation_for_placement is not None:
                # Exchange parameters i.e. Reset rule blueprint and modify the mujoco_object copy
                old_rotation = mujoco_object.rotation
                mujoco_object.rotation = mujoco_object_rule_blueprint.rotation
                mujoco_object_rule_blueprint.rotation = old_rotation

            mujoco_object.position = mujoco_object_rule_blueprint.position

            # If Site is area type, offset the coordinates to the boundaries
            if isinstance(site, Area):
                reference_boundaries = ((-site.environment.size[0], -site.environment.size[0]) , (site.environment.size[1], site.environment.size[1])) # TODO Not sure if this is correct and maybe we need to to /2 after a ticket
                mujoco_object.position = Utils.offset_coordinates_to_boundaries(mujoco_object.position, site.boundary, reference_boundaries=reference_boundaries)

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
        """Sample the amount of objects to be placed if amount is a tuple of different values.

        Parameters:
            amount (tuple[int, int]): Range of objects for randomization

        Returns:
            amount_int (int): Sample drawn from amount range
        """
        amount_int = (
            amount[0]
            if (amount[0] == amount[1])
            else np.random.randint(
                int(amount[0]), int(amount[1]) + 1
            )  # Randint function is exclusive on high val
        )
        return amount_int

    def _get_random_colors(
        self, amount: int, color_groups: Union[tuple[int, int], None]
    ) -> Union[list[list[float]], None]:
        """Returns a list of random rgba colors (with alpha=1).

        Parameters:
            amount (int): Number of objects
            color_groups (Union[tuple[int, int], None]): Range of members per distinctly colored group

        Returns:
            colors_for_placement (Union[list[list[float]], None]): List of randomized rgba colors
                (with duplicate entries for each group member, if color_groups > 1)
        """
        if color_groups is None:
            return None

        # Get list of available color names
        color_names = list(webcolors.CSS3_NAMES_TO_HEX.keys())

        # Get random int in range of colors
        colors_randint = (
            color_groups[0]
            if (color_groups[0] == color_groups[1])
            else np.random.randint(
                int(color_groups[0]), int(color_groups[1]) + 1
            )  # higher is excluding
        )

        # Get number of different colors needed by amount / color_groups
        colors_needed = int(
            amount / colors_randint
        )  # Int type cast automatically rounds down

        # Get random rgba for number of colors needed
        colors_rgba = list()

        # Shuffle color names
        random.shuffle(color_names)

        # Loop over the first 'colors_needed' colors and convert them to rgba
        # and normalize between 0 and 1
        for color in color_names[:colors_needed]:
            color_rgba = self._get_rgba_from_color_name(color)
            color_rgba_normalized = [(float(val) / 255) for val in color_rgba]
            colors_rgba.append(color_rgba_normalized)

        # Generate list of colors depending on amount an
        colors_for_placement = list()
        for color in colors_rgba:
            for _ in range(colors_randint):
                colors_for_placement.append(color)

        # Fill colors_for_placement list if amount of objects is greater than colors in the list.
        # This happens if amount % color_groups != 0
        while amount > len(colors_for_placement):
            sampled_color = sample(colors_rgba, 1)[0]
            colors_for_placement.append(sampled_color)

        return colors_for_placement

    def _get_random_sizes(
        self,
        amount: int,
        size_groups: Union[tuple[float, float], None],
        size_value_range: Union[tuple[float, float], None],
    ) -> Union[list[list[float]], None]:
        """Returns a list of random sizes.

        Parameters:
            amount (int): Number of objects
            size_groups (Union[tuple[float, float], None]): Range of members per distinctly sized group
            size_value_range (Union[tuple[float, float], None]): Defines the value size of the randomization process

        Returns:
            sizes_for_placement (Union[list(float, float, float), None]): List of randomized sizes
                (with duplicate entries for each group member, if size_groups > 1)
        """
        if size_groups is None:
            return None

        # Get random int in range of sizes
        sizes_randint = (
            size_groups[0]
            if (size_groups[0] == size_groups[1])
            else np.random.randint(
                int(size_groups[0]), int(size_groups[1]) + 1
            )  # Higher is excluding
        )

        # Get number of different sizes needed by amount / size_groups
        sizes_needed = int(
            amount / sizes_randint
        )  # Int type cast automatically rounds down

        # Get random sizes for number of sizes needed
        sizes = list()
        sizes_used = list()
        for _ in range(sizes_needed):
            random_size = self._get_size_array(size_value_range=size_value_range)
            while random_size in sizes_used:
                random_size = self._get_size_array(size_value_range=size_value_range)
            sizes_used.append(random_size)
            sizes.append(random_size)

        # Generate list of colors depending on amount an
        sizes_for_placement = list()
        for size in sizes:
            for _ in range(sizes_randint):
                sizes_for_placement.append(size)

        # Fill colors_for_placement list if amount of objects is greater than colors in the list.
        # This happens if amount % color_groups != 0
        while amount > len(sizes_for_placement):
            sampled_color = sample(sizes, 1)[0]
            sizes_for_placement.append(sampled_color)

        # Apply shuffling so that color and size is not synchronized
        random.shuffle(sizes_for_placement)

        return sizes_for_placement

    def _get_rgba_from_color_name(
        self, color_name: str
    ) -> Union[tuple[float, float, float, float], None]:
        """Takes color as argument and returns the corresponding rgba color code.

        Parameters:
            color_name (str): Name of color

        Returns:
            rgba (Union[tuple[float, float, float, float], None]): Rgba values for the corresponding color string
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

    def _get_size_array(
        self, size_value_range: tuple[float, float]
    ) -> list[float, float, float]:
        """Generates 3D random size in given range.

        Parameters:
            size_value_range (tuple[float, float]): Range of possible size values

        Returns:
            random_size (list[float, float, float]): Randomized size values in given range for 3D
        """
        x_rand_size_float = np.random.uniform(
            size_value_range[0], size_value_range[1]
        )  # Higher is excluding
        y_rand_size_float = np.random.uniform(
            size_value_range[0], size_value_range[1]
        )  # Higher is excluding
        z_rand_size_float = np.random.uniform(
            size_value_range[0], size_value_range[1]
        )  # Higher is excluding
        random_size = [x_rand_size_float, y_rand_size_float, z_rand_size_float]
        return random_size

    def _get_random_rotation(
        self, amount: int, z_rotation_range: Union[tuple[int, int], None]
    ) -> Union[list[float], None]:
        """Generate random number in z_rotation_range.

        Parameters:
            amount (int): Number of objects
            z_rotation_range (Union[tuple[int, int], None]): Range of degrees for randomization of z-axis

        Returns:
            z_rotations_for_placement (Union[list[float], None]): Random numbers in given range for z-axis rotation
        """
        if z_rotation_range is None:
            return None

        z_rotations_for_placement = list()
        for _ in range(amount):
            z_rotation = np.random.uniform(
                z_rotation_range[0], z_rotation_range[1]
            )  # Higher is excluding
            z_rotations_for_placement.append(z_rotation)
        return z_rotations_for_placement
