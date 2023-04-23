from abc import ABC, abstractmethod
from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class AbstractContainer(ABC):
    """Abstract class for environment and area"""

    @abstractmethod
    def __init__(self):
        """Initializes the Site class."""
        pass

    @abstractmethod
    def add(self, *, mujoco_object: MujocoObject):
        """Adds mujoco-object"""
        pass

    @abstractmethod
    def remove(self, *, mujoco_object: MujocoObject):
        """Removes mujoco-object"""
        pass

    @property
    @abstractmethod
    def name(self):
        """Get name"""
        pass

    @name.setter
    @abstractmethod
    def name(self, name: str):
        """Set name"""
        pass

    @property
    @abstractmethod
    def size(self):
        """Get size"""
        pass

    @property
    @abstractmethod
    def mjcf_model(self):
        """Get mjcf model"""
        pass

    @property
    @abstractmethod
    def mujoco_objects(self):
        """Get mujoco objects"""
        pass
