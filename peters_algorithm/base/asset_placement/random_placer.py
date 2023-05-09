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

    def __init__(
        self,
        distribution: PlacerDistribution = Placer2DDistribution(
            np.random.default_rng().multivariate_normal,
            (0, 0),
            np.array([[10, 0], [0, 10]]),
        ),
    ):
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
        validators: list[Validator],
        amount: tuple[int, int] = (1, 1),
    ):
        """Adds a mujoco object to a site by calling the sites add method.
        Possibly checks placement via the vlaidator.

        Parameters:
            site (AbstractContainer): Site class instance where the object is added to
            mujoco_object_blueprint (mjcf.RootElement): To-be-placed mujoco object
            validators (list): List of validator class instances used to check object placement
            amount (tuple): Range of possible amount of objects to be placed
        """

        # Sample the amount of objects to be placed if amount is a tuple and differ
        amount = (
            amount[0]
            if (amount[0] == amount[1])
            else np.random.randint(int(amount[0]), int(amount[1]))
        )
        for _ in range(amount):
            # Copy the blueprint to avoid changing the original
            mujoco_object = self._copy(mujoco_object_blueprint)

            # Old position is used to keep the z position
            old_position = mujoco_object.position

            # We only want to sample x and y, so we keep the old z position
            z_position = old_position[2]

            # Sample a new position
            mujoco_object.position = [*self.distribution(), z_position]

            count = 0
            # Ask every validator for approval until all approve or MAX_TRIES is reached, then throw error
            while not all(
                [validator.validate(mujoco_object) for validator in validators]
            ):
                count += 1
                if count >= RandomPlacer.MAX_TRIES:
                    raise RuntimeError(
                        "Placement has failed {} times, please check your config.yaml".format(
                            RandomPlacer.MAX_TRIES
                        )
                    )
                # If placement is not possible, sample a new position
                mujoco_object.position = [*self.distribution(), old_position[2]]

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
