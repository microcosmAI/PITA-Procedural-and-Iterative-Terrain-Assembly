import random
import logging
from tqdm import tqdm
from typing import Union
from pita_algorithm.base.asset_placement.validator import Validator
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from pita_algorithm.base.asset_placement.abstract_placer import AbstractPlacer
from pita_algorithm.utils.object_property_randomization import (
    ObjectPropertyRandomization,
)
from pita_algorithm.base.world_sites.area import Area
from pita_algorithm.base.world_sites.environment import Environment


class FixedPlacer(AbstractPlacer):
    """Places objects in a fixed manner."""

    def __init__(self):
        """Constructor of the FixedPlacer class."""
        pass

    def add(
        self,
        site: AbstractSite,
        mujoco_object_blueprint: MujocoObject,
        mujoco_object_rule_blueprint: MujocoObject,
        validators: list[Validator],
        amount: int,
        coordinates: list[list[float, float, float]],
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
            site (AbstractSite): AbstractSite class instance where the object is added to
            mujoco_object_blueprint (MujocoObject): Blueprint of to-be-placed mujoco object
            mujoco_object_rule_blueprint (MujocoObject): To-be-checked mujoco object
            validators (list[Validator]): Validator class instance used to check object placement
            amount (int): Amount of object to be placed.
            coordinates (list[list[float, float, float]]): List of coordinate lists where each object is placed
            z_rotation_range (Union[tuple[int, int], None]): Range of degrees for z-axis rotation
            color_groups (Union[tuple[int, int], None]): Range of possible different colors for object
            size_groups (Union[tuple[int, int], None]): Range of possible different sizes for object
            size_value_range (Union[tuple[float, float], None]): Range of size values allowed in randomization
            asset_pool (Union[list, None]): List of xml-names of assets which should be sampled from
            mujoco_objects_blueprints (Union[dict, None]): Dictionary of all objects as mujoco-objects
        """
        logger = logging.getLogger()
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

        for obj_idx in tqdm(range(amount)):
            # Sample from asset pool if asset_pool is given by user
            if asset_pool is not None:
                asset_name = random.choice(asset_pool).split(".xml")[0]
                mujoco_object_rule_blueprint = self._copy(
                    mujoco_objects_blueprints[asset_name]
                )
                mujoco_object_blueprint = self._copy(
                    mujoco_objects_blueprints[asset_name]
                )

            # Set the position of the object to the user specified relative coordinates
            x_min = float
            y_min = float
            if isinstance(site, Environment):
                x_min = -site.size[0]
                y_min = -site.size[1]
            elif isinstance(site, Area):
                x_min = site.boundary[0][0]
                y_min = site.boundary[0][1]
            x_length = 2 * site.size[0]
            y_width = 2 * site.size[1]
            (relative_x, relative_y, z) = coordinates[obj_idx]
            (absolute_x, absolute_y) = (
                relative_x / 100 * x_length,
                relative_y / 100 * y_width,
            )
            new_x, new_y = (x_min + absolute_x, y_min + absolute_y)
            new_coords = [float(new_x), float(new_y), float(z)]
            mujoco_object_rule_blueprint.position = new_coords

            if not colors_for_placement is None:
                # Apply colors to objects
                mujoco_object_rule_blueprint.color = colors_for_placement[obj_idx]

            if not sizes_for_placement is None:
                # Apply sizes to objects
                mujoco_object_rule_blueprint.size = sizes_for_placement[obj_idx]

            if not z_rotation_for_placement is None:
                # Apply rotation to z-axis of object
                rotation = mujoco_object_rule_blueprint.rotation
                if rotation is None:
                    rotation = [0, 0, z_rotation_for_placement[obj_idx]]
                else:
                    rotation[2] = z_rotation_for_placement[obj_idx]
                mujoco_object_rule_blueprint.rotation = rotation

            if not all(
                [
                    val.validate(mujoco_object=mujoco_object_rule_blueprint, site=site)
                    for val in validators
                ]
            ):
                logger.error(
                    "User specified placement of object '{}' at '{}' in site '{}' could not be satisfied.".format(
                        mujoco_object_rule_blueprint.name,
                        mujoco_object_rule_blueprint.position,
                        site.name,
                    )
                )
                raise RuntimeError(
                    "User specified placement of object '{}' at '{}' in site '{}' could not be satisfied.".format(
                        mujoco_object_rule_blueprint.name,
                        mujoco_object_rule_blueprint.position,
                        site.name,
                    )
                )

            # Copy the blueprint to avoid changing the original
            mujoco_object = self._copy(mujoco_object_blueprint)
            mujoco_object.position = mujoco_object_rule_blueprint.position

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

            # Keep track of the placement in the validators
            for validator in validators:
                validator.add(mujoco_object)

            # Add the object to the site
            site.add(mujoco_object=mujoco_object)

    def remove(self, site: AbstractSite, mujoco_object: MujocoObject):
        """Removes a mujoco object from a site by calling the sites remove method.
        Possibly checks placement via the validator.

        Parameters:
            site (Site): Site class instance where the object is removed from
            mujoco_object (MujocoObject): To-be-removed mujoco object
        """
        site.remove(mujoco_object=mujoco_object)
