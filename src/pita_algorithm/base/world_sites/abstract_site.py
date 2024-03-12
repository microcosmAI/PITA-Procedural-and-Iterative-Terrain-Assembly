from abc import ABC, abstractmethod
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class AbstractSite(ABC):
    """Abstract class for environment and area."""

    @abstractmethod
    def __init__(self):
        """Constructor of the AbstractSite class."""
        pass

    @abstractmethod
    def add(self, mujoco_object: MujocoObject):
        """Adds mujoco-object.

        Parameters:
            mujoco_object (MujocoObject): Mujoco object to add to site
        """
        pass

    @abstractmethod
    def remove(self, mujoco_object: MujocoObject):
        """Removes mujoco-object.

        Parameters:
            mujoco_object (MujocoObject): Mujoco object to remove from site
        """
        pass

    @property
    @abstractmethod
    def name(self):
        """Get name."""
        pass

    @name.setter
    @abstractmethod
    def name(self, name: str):
        """Set name.

        Parameters:
            name (str): Name of site
        """
        pass

    @property
    @abstractmethod
    def size(self):
        """Get size."""
        pass

    @property
    @abstractmethod
    def mjcf_model(self):
        """Get mjcf model."""
        pass

    @property
    @abstractmethod
    def mujoco_objects(self):
        """Get mujoco objects."""
        pass
