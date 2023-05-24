from dm_control import mjcf

from peters_algorithm.base.world_container.environment import Environment
from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from peters_algorithm.base.world_container.abstract_container import AbstractContainer


class Area(AbstractContainer):
    """Area object class"""

    def __init__(self, *, name: str, size: tuple[float, float, float], environment: Environment, boundary: tuple):
        """Initialize area

        Parameters:
            name (str): Name of area
            size (tuple): Size of area
            mujoco_objects (dict): Dictionary of mujoco objects in area
            environment (Environment): Environment class instance
            boundary (tuple): Boundary of the area that constrains object placement
        """
        self._name = name
        self._size = size
        self._mjcf_model = environment.mjcf_model
        # self._mjcf_model.worldbody.add("geom", name="base_plane_area", type="plane", size=self._size)
        self._mujoco_objects = {}
        self._boundary = boundary

    def add(self, *, mujoco_object: MujocoObject):
        """Add object to area-mjcf and mujoco-object dictionary of area. Also sets name of object to the one given by mujoco

        Parameters:
            mujoco_object (MujocoObject): Mujoco object to add to area-mjcf and area-dictionary
        """
        # The attach() method returns the attachement frame (i.e. a body with the attached mujoco object)
        attachement_frame = self._mjcf_model.attach(mujoco_object.mjcf_obj)
        # By calling all_children() on the attachement frame, we can access their uniqe identifier
        mujoco_object.xml_id = (
            attachement_frame.all_children()[0].full_identifier
        )

        # Check for free joints (either <joint type="free"/> or <freejoint/> but always as a direct child)
        # If present, remove it and add it again one level above
        joint_list = attachement_frame.all_children()[0].find_all("joint", immediate_children_only=True)
        if joint_list:
            if joint_list[0].tag == "freejoint" or joint_list[0].type == "free":
                joint_attribute_dict = joint_list[0].get_attributes()
                joint_attribute_dict.pop("type", None)  # pop type key if present
                attachement_frame.add("joint", type="free", **joint_attribute_dict)
                joint_list[0].remove()

        self._mujoco_objects[mujoco_object.xml_id] = mujoco_object

    def remove(self, *, mujoco_object: MujocoObject):
        """Removes object from area-mjcf and from mujoco-object dictionary of area

        Parameters:
            mujoco_object (MujocoObject): Mujoco object to remove from area-mjcf and area-dictionary
        """
        mujoco_object.mjcf_obj.detach()
        del self._mujoco_objects[mujoco_object.xml_id]

    @property
    def name(self):
        """Get name"""
        return self._name

    @name.setter
    def name(self, name: str):
        """Set name"""
        self._name = name

    @property
    def size(self):
        """Get size

        Returns:
            size (tuple): Size of area
        """
        return self._size

    @property
    def mjcf_model(self):
        """Get mjcf model

        Returns:
            mjcf_model (mjcf): Mjcf model of area
        """
        return self._mjcf_model

    @property
    def mujoco_objects(self):
        """Get mujoco objects

        Returns:
            mujoco_objects (dict): Dictionary of mujoco objects in area
        """
        return self._mujoco_objects

    @property
    def boundary(self):
        """Get area boundary

        Returns:
            boundary (tuple): Tuple with the area boundary
        """
        return self._boundary

    @boundary.setter
    def boundary(self, boundary: tuple):
        """Set boundary"""
        self.boundary = boundary
