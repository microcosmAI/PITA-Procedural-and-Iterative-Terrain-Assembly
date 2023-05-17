import random
import numpy as np
from typing import Callable

from peters_algorithm.base.asset_placement.validator import Validator
from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from peters_algorithm.base.asset_placement.abstract_placer import AbstractPlacer
from peters_algorithm.base.world_container.abstract_container import AbstractContainer


class GlobalNamespace:
    """Placeholder until we know how to name objects, before attaching them"""

    counter = 0

    @staticmethod
    def get():
        """Get a unique name

        Returns:
            (str): unique name
        """
        GlobalNamespace.counter += 1
        return str(GlobalNamespace.counter)


class PlacerDistribution:
    """Class for holing Distribution with specific parameterizations"""

    def __init__(self, distribution: Callable, *args):
        """Initialize a distribution for use in the RandomPlacer. The distribution
        object will be called with *args as paramters.
        Write for instance:
        `PlacerDistribution(np.random.default_rng().normal, 2, 1)` if you intend
        to sample from a normal distribution with loc=2 and scale = 1
        The samples will be drawn independently, which results in square like shapes.

        Parameters:
            distribution (Callable): distribution(*args) will be used for sampling values
            *args (sequence of floats): parameters for the random distribution
        """
        self.distribution = distribution
        self.parameters = args

    def __call__(self):
        """Draws samples from the distribution

        Returns:
            (float, float): sampled x and y coordinates
        """
        return self.distribution(*self.parameters), self.distribution(*self.parameters)


class Placer2DDistribution(PlacerDistribution):
    """Class for two dimensional distributions, otherwise equivalent to its parent class"""

    def __call__(self):
        """Draw a sample from the distribution

        Returns:
            (float, float): sampled x and y coordinates
        """
        x, y = self.distribution(*self.parameters)
        return (x, y)


class CircularUniformDistribution(PlacerDistribution):
    """Class for holing Distribution with specific parameterizations"""

    def __init__(self, loc: float = 0, scale: float = 10.0):
        """Distribution for uniformly drawing samples from a circle

        Parameters:
            loc (float): minimal euclidean distance from the center
            scale (float): maximal euclidean distance from the center
        """
        self.loc = loc
        self.scale = scale

    def __call__(self):
        """Draw a sample from the distribution

        Returns:
            (float, float): sampled x and y coordinates
        """
        length = np.sqrt(np.random.uniform(self.loc, self.scale**2))
        angle = np.pi * np.random.uniform(0, 2)

        x = length * np.cos(angle)
        y = length * np.sin(angle)
        return x, y


class RandomPlacer(AbstractPlacer):
    """A placer that is meant for procedural and random map generation"""

    # The validator does not check, if the addition of an item is possible. Instead, after placement
    # has failed for MAX_TRIES times, an error gets thrown. MAX_TRIES could alternatively be implemented
    # dynamically, as a field of any Placer instantiation
    MAX_TRIES = 10000

    def __init__(self, distribution: PlacerDistribution):
        """Initializes the Placer class. From the distribution a translation on the x and y axis will be
        respectively sampled. So the distribution of the to be placed objects is actually centered at
        the position of the original object plus a loc parameter of the distribution (if it has one).
        Note, that this will result in square shaped distributions, unless an explicitly circular
        distribution is used.

        Parameters:
            distribution (PlacerDistribution): Distribution from which placement randomness will be sampled
        """
        self.distribution = distribution

    def add(
        self,
        site: AbstractContainer,
        mujoco_object_blueprint: MujocoObject,
        mujoco_objects_rule_blueprint: MujocoObject,
        validators: list[Validator],
        amount: tuple[int, int] = (1, 1),
        colors_range: tuple[int, int] = None,
        sizes_range: tuple[int, int] = None,
    ):
        """Adds a mujoco object to a site by calling the sites add method.
        Possibly checks placement via the vlaidator.

        Parameters:
            site (AbstractContainer): Site class instance where the object is added to
            mujoco_object_blueprint (mjcf.RootElement): To-be-placed mujoco object
            mujoco_objects_rule_blueprint (mjcf.RootElement): To-be-checked mujoco object
            validators (list): List of validator class instances used to check object placement
            amount (tuple): Range of possible amount of objects to be placed
            colors_range (tuple): Range of possible different colors for object
            sizes_range (tuple): Range of possible different sizes for object
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
                    mujoco_object_blueprint.color = colors_rgba[randint]
                else:
                    mujoco_object_blueprint.color = colors_rgba[i]

            if not sizes is None:
                # appy sizes to objects
                if i > (len(sizes) - 1):
                    randint = random.randrange(len(sizes))
                    mujoco_object_blueprint.size = sizes[randint]
                else:
                    mujoco_object_blueprint.size = sizes[i]

            # Old position is used to keep the z position
            old_position = mujoco_object_blueprint.position

            # We only want to sample x and y, so we keep the old z position
            z_position = old_position[2]

            # Sample a new position
            mujoco_object_blueprint.position = [*self.distribution(), z_position]

            count = 0
            # Ask every validator for approval until all approve or MAX_TRIES is reached, then throw error
            while not all(
                [
                    validator.validate(mujoco_object_blueprint, site)
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
                mujoco_object_blueprint.position = [
                    *self.distribution(),
                    old_position[2],
                ]

            # Copy the blueprint to avoid changing the original
            mujoco_object = self._copy(mujoco_object_blueprint)

            if colors_rgba is not None:
                # Exchange parameters i.e. Reset rule blueprint and modify the mujoco_object copy
                old_color = mujoco_object.color
                old_size = mujoco_object.size

                mujoco_object.color = mujoco_objects_rule_blueprint.color
                mujoco_object.size = mujoco_objects_rule_blueprint.size

                mujoco_objects_rule_blueprint.color = old_color
                mujoco_objects_rule_blueprint.size = old_size

            mujoco_object_blueprint.position = mujoco_objects_rule_blueprint.position

            # Keep track of the placement in the validators
            for validator in validators:
                validator.add(mujoco_object)

            # Add the object to the site
            site.add(mujoco_object=mujoco_object)

    def remove(self, site: AbstractContainer, mujoco_object: MujocoObject):
        """Removes a mujoco object from a site by calling the sites remove method.
        Possibly checks placement via the validator.

        Parameters:
            site (AbstractContainer): Site class instance where the object is removed from
            mujoco_object (mjcf.RootElement): To-be-removed mujoco object
        """
        site.remove(mujoco_object=mujoco_object)

    @staticmethod
    def _get_random_colors(colors_range: tuple[int, int]):
        """Gets a list of random rgba colors (with alpha=1) with a random amount in given range.
           Every color is added twice to the list, since the ball pit scenario requires color pairs of balls.

        Parameters:
            colors_range (tuple[int, int]): range of different colors

        Returns:
            colors_rgba (list(tuple[float, float, float, float]): list of randomized rgba colors
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
            random_rgba = [
                round(np.random.random(), 2),
                round(np.random.random(), 2),
                round(np.random.random(), 2),
                1,
            ]  # transparency set to 1
            colors_rgba.append(random_rgba)
            colors_rgba.append(
                random_rgba
            )  # append twice to have pairs of colors for ball pit scenario

        return colors_rgba

    @staticmethod
    def _get_random_sizes(sizes_range: tuple[float, float]):
        """Gets a list of random sizes with a random amount in given range.
           Every size is added twice to the list, since the ball pit scenario requires size pairs of balls.

        Parameters:
            sizes_range (tuple[int, int]): range of different sizes

        Returns:
            sizes (list(float)): list of randomized sizes between 0 and 2
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
            sizes.append(random_size)
            sizes.append(random_size)

        return sizes
