import random
import numpy as np
from typing import Callable, Union, Any

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
        colors_range: Union[tuple[int, int], None] = None,
        sizes_range: Union[tuple[int, int], None] = None,
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

        # Sample the amount of objects to be placed if amount is a tuple and differ
        amount = (
            amount[0]
            if (amount[0] == amount[1])
            else np.random.randint(int(amount[0]), int(amount[1]))
        )

        # get colors rgba
        colors_rgba = self._get_random_colors(colors_range=colors_range)
        if not colors_rgba is None:
            if len(colors_rgba) > amount:
                raise ValueError("Not enough objects for specified colors.")

        # get object size
        sizes = self._get_random_sizes(sizes_range=sizes_range)
        if not sizes is None:
            if len(sizes) > amount:
                raise ValueError("Not enough objects for specified sizes.")

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
    def _get_random_colors(
        colors_range: Union[tuple[int, int], None]
    ) -> Union[list[tuple[float, float, float, float]], None]:
        """Returns a list of random rgba colors (with alpha=1).
           Every color is added twice to the list.

        Parameters:
            colors_range (Union[tuple[float, float], None]): Range of different colors

        Returns:
            colors_rgba (Union[list[tuple[float, float, float, float]], None]): List of randomized rgba colors
        """
        if colors_range is None:
            return None

        # get random int in range of colors
        colors_randint = (
            colors_range[0]
            if (colors_range[0] == colors_range[1])
            else np.random.randint(int(colors_range[0]), int(colors_range[1]))
        )

        # get random rgba for every color existing
        colors_rgba = list()
        for _ in range(colors_randint):
            random_rgba = (
                round(np.random.random(), 2),
                round(np.random.random(), 2),
                round(np.random.random(), 2),
                1.0,
            )  # transparency set to 1
            colors_rgba.append(random_rgba)
            colors_rgba.append(
                random_rgba
            )  # append twice to have pairs of colors for ball pit scenario

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
