from abc import ABC, abstractmethod
from .site import Site
from .mujoco_object import MujocoObject

class Validator(ABC):
    def __init__(self):
        """Initializes the Validator class."""
        pass

    def validate(self, site: Site, mujoco_object: MujocoObject):
        """
        Validates the placement of a mujoco object on a site.

        Parameters:
            site (Site): Site class instance where the object is added to
            mujoco_object (MujocoObject): To-be-placed mujoco object
        """
        pass