import numpy as np
from dm_control import mjcf

from pita_algorithm.base.world_sites.environment import Environment
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from pita_algorithm.utils.general_utils import Utils


class Area(AbstractSite):
    """Represents an area in the environment. An area is a part of
    the environment that can contain objects.
    """

    def __init__(
        self,
        name: str,
        size: tuple[float, float, float],
        environment: Environment,
        boundary: tuple = None,
    ):
        """Initializes area.

        Parameters:
            name (str): Name of the area
            size (tuple): Size of the area
            mujoco_objects (dict): Dictionary of mujoco objects in the area
            environment (Environment): Environment class instance
            boundary (tuple): Boundary of the area that constrains object placement
        """
        self._name = name
        self._size = size
        self._mjcf_model = environment.mjcf_model
        self._mujoco_objects = {}
        self._boundary = boundary
        self.environment = environment

    def add(self, mujoco_object: MujocoObject):
        """Add object to the area _mjcf_model and its mujoco-object dictionary.
        Also sets the name of the object to the one given by mujoco.

        Parameters:
            mujoco_object (MujocoObject): Mujoco object to add
        """
        # Offset the coordinates to the boundaries of the area
        # mujoco_object.position = Utils.offset_coordinates_to_boundaries(mujoco_object.position) # TODO check if it mighrt be better to do this in the mujoco_object class

        # The attach() method returns the attachement frame
        # i.e., a body with the attached mujoco object
        attachement_frame = self._mjcf_model.attach(mujoco_object.mjcf_obj)
        # By calling all_children() on the attachement frame, we can access their uniqe identifier
        mujoco_object.xml_id = attachement_frame.all_children()[0].full_identifier

        # Check for free joints (<joint type="free"/> or <freejoint/> but always as a direct child)
        # If present, remove it and add it again one level above
        joint_list = attachement_frame.all_children()[0].find_all(
            "joint", immediate_children_only=True
        )
        if joint_list:
            if joint_list[0].tag == "freejoint" or joint_list[0].type == "free":
                joint_attribute_dict = joint_list[0].get_attributes()
                joint_attribute_dict.pop("type", None)  # pop type key if present
                attachement_frame.add("joint", type="free", **joint_attribute_dict)
                joint_list[0].remove()

        self._mujoco_objects[mujoco_object.xml_id] = mujoco_object

    def remove(self, mujoco_object: MujocoObject):
        """Removes object from the area _mjcf_model and its mujoco-object dictionary.

        Parameters:
            mujoco_object (MujocoObject): Mujoco object to remove
        """
        mujoco_object.mjcf_obj.detach()
        del self._mujoco_objects[mujoco_object.xml_id]

    @property
    def name(self) -> str:
        """Get name.

        Returns:
            name (str): Name of the area
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Set name.

        Parameters:
            name (str): Name of the area"""
        self._name = name

    @property
    def size(self) -> tuple[float, float, float]:
        """Get size.

        Returns:
            size (tuple[float, float, float]): Size of area
        """
        return self._size

    @property
    def mjcf_model(self) -> mjcf.RootElement:
        """Get mjcf model.

        Returns:
            mjcf_model (mjcf): Mjcf model of area
        """
        return self._mjcf_model

    @property
    def mujoco_objects(self) -> dict:
        """Get mujoco objects.

        Returns:
            mujoco_objects (dict): Dictionary of mujoco objects in area
        """
        return self._mujoco_objects

    @property
    def boundary(self):
        """Get area boundary.

        Returns:
            boundary (tuple): Tuple with the area boundary
        """
        return self._boundary

    @boundary.setter
    def boundary(self, boundary: tuple):
        """Set boundary.

        Parameters:
            boundary (tuple): Tuple with the area boundary
        """
        self.boundary = boundary
