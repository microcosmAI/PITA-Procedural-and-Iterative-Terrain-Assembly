from abc import ABC, abstractmethod
from dm_control import mjcf
import Validator
import Site


class Placer(ABC):
    @abstractmethod
    def __init__(self):
        """Initializes the Placer class."""
        pass

    @abstractmethod
    def add(
        self, site: Site, mujoco_object_blueprint: mjcf.RootElement, validator: list[Validator]
    ):
        """
        Adds a mujoco object to a site by calling the sites add method.
        Possibly checks placement via the vlaidator.

        Parameters:
            site (Site): Site class instance where the object is added to
            mujoco_object_blueprint (mjcf.RootElement): To-be-placed mujoco object
            validator (Validator): Validator class instance used to check object placement
        """
        site.add(mujoco_object_blueprint)

    @abstractmethod
    def remove(self, site: Site, mujoco_object: mjcf.RootElement):
        """
        Removes a mujoco object from a site by calling the sites remove method.
        Possibly checks placement via the vlaidator.

        Parameters:
            site (Site): Site class instance where the object is removed from
            mujoco_object (mjcf.RootElement): To-be-removed mujoco object
        """
        site.remove(mujoco_object)
