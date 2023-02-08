from abc import ABC, abstractmethod
from .mujoco_object import MujocoObject


class Site(ABC):
    """  abstract class for environment and area """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add(self, mujoco_object: MujocoObject):
        """ adds mujoco-object """
        pass

    @abstractmethod
    def remove(self, mujoco_object: MujocoObject):
        """ removes mujoco-object """
        pass

    @property
    @abstractmethod
    def name(self):
        """ get name """
        pass

    @name.setter
    @abstractmethod
    def name(self, name: str):
        """ set name """
        pass

    @property
    @abstractmethod
    def size(self):
        """ get size """
        pass

    @property
    @abstractmethod
    def mjcf_model(self):
        """ get mjcf model """
        pass

    @property
    @abstractmethod
    def mujoco_objects(self):
        """ get mujoco objects """
        pass
