import copy
from abc import ABC, abstractmethod
from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from peters_algorithm.base.asset_placement.validator import Validator
from peters_algorithm.base.world_container.abstract_container import AbstractContainer


class AbstractPlacer(ABC):
    @abstractmethod
    def __init__(self):
        """Initializes the Placer class."""
        pass

    def _copy(self, mujoco_object_blueprint: MujocoObject) -> MujocoObject:
        """Creates a copy of a mujoco object blueprint

        Parameters:
            mujoco_object_blueprint (MujocoObject): To-be-copied mujoco object

        Returns:
            mujoco_object (MujocoObject): Copy of the mujoco object blueprint
        """
        mujoco_object = copy.deepcopy(mujoco_object_blueprint)
        # TODO NameGenerator
        # TODO modify references to relevant object attributes like size/pos
        return mujoco_object

    @abstractmethod
    def add(
        self,
        *,
        site: AbstractContainer,
        mujoco_object_blueprint: MujocoObject,
        validator: list[Validator]
    ):
        """Adds a mujoco object to a site by calling the sites add method.
        Possibly checks placement via the validator.

        Parameters:
            site (AbstractContainer): Site class instance where the object is added to
            mujoco_object_blueprint (MujocoObject): To-be-placed mujoco object
            validator (Validator): Validator class instance used to check object placement

        Returns:
            site (AbstractContainer): Site class instance where the object is added to (with added mjcf-obj)
        """
        mujoco_object = self._copy(mujoco_object_blueprint)
        site.add(mujoco_object=mujoco_object)

    @abstractmethod
    def remove(self, *, site: AbstractContainer, mujoco_object: MujocoObject):
        """Removes a mujoco object from a site by calling the sites remove method.
        Possibly checks placement via the validator.

        Parameters:
            site (AbstractContainer): Site class instance where the object is removed from
            mujoco_object (MujocoObject): To-be-removed mujoco object

        Returns:
            site (AbstractContainer): Site class instance where the object is added to (with removed mjcf-obj)
        """
        site.remove(mujoco_object=mujoco_object)
