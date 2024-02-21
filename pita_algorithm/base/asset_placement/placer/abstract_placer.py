import copy
import logging
from typing import Union
from abc import ABC, abstractmethod
from pita_algorithm.base.asset_placement.validator import Validator
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class AbstractPlacer(ABC):
    """Abstract class for object placers."""

    @abstractmethod
    def __init__(self):
        """Constructor of the AbstractPlacer class."""
        pass

    @staticmethod
    def _copy(mujoco_object_blueprint: MujocoObject) -> MujocoObject:
        """Creates a copy of a mujoco object blueprint.

        Parameters:
            mujoco_object_blueprint (MujocoObject): To-be-copied mujoco object

        Returns:
            mujoco_object (MujocoObject): Copy of the mujoco object blueprint
        """
        mujoco_object = copy.deepcopy(mujoco_object_blueprint)

        return mujoco_object

    @staticmethod
    def _check_user_input(
        color_groups: Union[tuple[int, int], None],
        size_groups: Union[tuple[int, int], None],
        amount: int,
    ) -> None:
        """Checks if color_groups and size_groups is compatible with amount.

        Parameters:
            color_groups (Union[tuple[int, int], None]): Range of possible different colors for object
            size_groups (Union[tuple[int, int], None]): Range of possible different sizes for object
            amount (int): Amount of object to be placed.
        """
        logger = logging.getLogger()

        if color_groups is not None:
            if max(color_groups) > amount:
                logger.error(
                    f"Not enough objects for specified colors. Objects: {amount}, Colors: {color_groups}."
                )
                raise ValueError(
                    f"Not enough objects for specified colors. Objects: {amount}, Colors: {color_groups}."
                )

        if size_groups is not None:
            if len(size_groups) > amount:
                logger.error(
                    f"Not enough objects for specified sizes. Objects: {amount}, Sizes: {size_groups}."
                )
                raise ValueError(
                    f"Not enough objects for specified sizes. Objects: {amount}, Sizes: {size_groups}."
                )

    @abstractmethod
    def add(
        self,
        site: AbstractSite,
        mujoco_object_blueprint: MujocoObject,
        validators: list[Validator],
        amount: Union[int, tuple],
        coordinates: list[list[float, float, float]],
        z_rotation_range: Union[tuple[int, int], None] = None,
        color_groups: Union[tuple[int, int], None] = None,
        size_groups: Union[tuple[int, int], None] = None,
        size_value_range: Union[tuple[int, int], None] = None,
        asset_pool: Union[list, None] = None,
        mujoco_objects_blueprints: Union[dict, None] = None,
    ) -> None:
        """
        Parameters:
            site (AbstractSite): AbstractSite class instance where the object is added to
            mujoco_object_blueprint (MujocoObject): Blueprint of to-be-placed mujoco object
            validators (list[Validator]): Validator class instance used to check object placement
            amount (int, tuple): Amount of object to be placed
            coordinates (list[list[float, float, float]]): List of coordinate lists where each object is placed
            z_rotation_range (Union[tuple[int, int], None]): Range of degrees for z-axis rotation
            color_groups (Union[tuple[int, int], None]): Range of possible different colors for object
            size_groups (Union[tuple[int, int], None]): Range of possible different sizes for object
            size_value_range (Union[tuple[float, float], None]): Range of size values allowed in randomization
            asset_pool (Union[list, None]): List of xml-names of assets which should be sampled from
            mujoco_objects_blueprints (Union[dict, None]): Dictionary of all objects as mujoco-objects
        """
        mujoco_object = self._copy(mujoco_object_blueprint)
        site.add(mujoco_object=mujoco_object)

    @abstractmethod
    def remove(self, site: AbstractSite, mujoco_object: MujocoObject) -> None:
        """Removes a mujoco object from a site by calling the sites remove method.

        Parameters:
            site (AbstractSite): Site class instance where the object is removed from
            mujoco_object (MujocoObject): To-be-removed mujoco object
        """
        site.remove(mujoco_object=mujoco_object)
