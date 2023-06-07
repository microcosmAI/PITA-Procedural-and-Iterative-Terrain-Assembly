import copy
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

    def _copy(self, mujoco_object_blueprint: MujocoObject) -> MujocoObject:
        """Creates a copy of a mujoco object blueprint.

        Parameters:
            mujoco_object_blueprint (MujocoObject): To-be-copied mujoco object

        Returns:
            mujoco_object (MujocoObject): Copy of the mujoco object blueprint
        """
        mujoco_object = copy.deepcopy(mujoco_object_blueprint)

        return mujoco_object

    @abstractmethod
    def add(
        self,
        site: AbstractSite,
        mujoco_object_blueprint: MujocoObject,
        validators: list[Validator],
    ):
        """Adds a mujoco object to a site by calling the sites add method.
        Possibly checks placement via the validator.

        Parameters:
            site (AbstractSite): Site class instance where the object is added to
            mujoco_object_blueprint (MujocoObject): To-be-placed mujoco object
            validators (list): List of validator class instances used to check object placement
        """
        mujoco_object = self._copy(mujoco_object_blueprint)
        site.add(mujoco_object=mujoco_object)

    @abstractmethod
    def remove(self, site: AbstractSite, mujoco_object: MujocoObject):
        """Removes a mujoco object from a site by calling the sites remove method.
        Possibly checks placement via the validator.

        Parameters:
            site (AbstractSite): Site class instance where the object is removed from
            mujoco_object (MujocoObject): To-be-removed mujoco object
        """
        site.remove(mujoco_object=mujoco_object)
