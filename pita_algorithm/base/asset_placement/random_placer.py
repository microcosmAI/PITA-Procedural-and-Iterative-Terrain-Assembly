import logging
import random
import numpy as np
from tqdm import tqdm
from typing import Callable, Union, Any
from pita_algorithm.base.asset_placement.validator import Validator
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from pita_algorithm.base.asset_placement.abstract_placer import AbstractPlacer
from pita_algorithm.utils.object_property_randomization import (
    ObjectPropertyRandomization,
)
from pita_algorithm.base.asset_placement.abstract_placer_distribution import (
    AbstractPlacerDistribution,
)
from pita_algorithm.base.world_sites.area import Area
from pita_algorithm.base.world_sites.environment import Environment
from pita_algorithm.utils.general_utils import Utils
from pita_algorithm.utils.object_property_randomization import (
    ObjectPropertyRandomization,
)


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
        asset_pool: Union[list, None] = None,
        mujoco_objects_blueprints: Union[dict, None] = None,
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
            asset_pool (Union[list, None]): List of xml-names of assets which should be sampled from
            mujoco_objects_blueprints (Union[dict, None]): Dictionary of all objects as mujoco-objects
        """
        logger = logging.getLogger()

        # Sample from amount range
        amount: int = ObjectPropertyRandomization.sample_from_amount(amount=amount)

        # Get colors rgba
        if not color_groups is None:
            if max(color_groups) > amount:
                logger.error(
                    f"Not enough objects for specified colors. Objects: {amount}, Colors: {color_groups}."
                )
                raise ValueError(
                    f"Not enough objects for specified colors. Objects: {amount}, Colors: {color_groups}."
                )
        colors_for_placement = ObjectPropertyRandomization.get_random_colors(
            amount=amount, color_groups=color_groups
        )

        # Get object size
        if not size_groups is None:
            if len(size_groups) > amount:
                logger.error(
                    f"Not enough objects for specified sizes. Objects: {amount}, Sizes: {size_groups}."
                )
                raise ValueError(
                    f"Not enough objects for specified sizes. Objects: {amount}, Sizes: {size_groups}."
                )
        sizes_for_placement = ObjectPropertyRandomization.get_random_sizes(
            amount=amount, size_groups=size_groups, size_value_range=size_value_range
        )

        # Get object z-axis rotation
        z_rotation_for_placement = ObjectPropertyRandomization.get_random_rotation(
            amount=amount, z_rotation_range=z_rotation_range
        )

        for i in tqdm(range(amount)):
            # Sample from asset pool if asset_pool is given by user
            if asset_pool is not None:
                asset_name = random.choice(asset_pool).split(".xml")[0]
                mujoco_object_rule_blueprint = self._copy(
                    mujoco_objects_blueprints[asset_name]
                )
                mujoco_object_blueprint = self._copy(
                    mujoco_objects_blueprints[asset_name]
                )

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
                    logger.error(
                        "Placement of object '{}' in site '{}' has failed '{}' times, please check your config.yaml".format(
                            mujoco_object_blueprint.name,
                            site.name,
                            RandomPlacer.MAX_TRIES,
                        )
                    )
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
                reference_boundaries = (
                    (-site.environment.size[0], -site.environment.size[0]),
                    (site.environment.size[1], site.environment.size[1]),
                )  # TODO Not sure if this is correct and maybe we need to to /2 after a ticket
                mujoco_object.position = Utils.offset_coordinates_to_boundaries(
                    mujoco_object.position,
                    site.boundary,
                    reference_boundaries=reference_boundaries,
                )

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
