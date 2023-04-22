from dm_control import mjcf
from peters_algorithm.base.world.abstract_base_plane import AbstractBasePlane
from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class Area(AbstractBasePlane):
    """Area object class"""

    def __init__(self, *, name: str, size: tuple[float, float, float]):
        """Initialize area

        Parameters:
            name (str): Name of area
            size (tuple): Size of area
            mjcf_model (mjcf): Mjcf model of area
            mujoco_objects (dict): Dictionary of mujoco objects in area
        """
        self._name = name
        self._size = size
        self._mjcf_model = self._initialize_area()
        self._mujoco_objects = {}

    def _initialize_area(self):
        """Initialize area

        Returns:
            mjcf_model (mjcf): Mjcf-object of area
        """
        self._mjcf_model = mjcf.RootElement(model=self.name)
        # self._mjcf_model.worldbody.add("geom", name="base_plane_area", type="plane", size=self._size)
        return self._mjcf_model

    def add(self, *, mujoco_object: MujocoObject):
        """Add object to area-mjcf and to mujoco-object dictionary of area

        Parameters:
            mujoco_object (MujocoObject): Mujoco object to add to area-mjcf and area-dictionary
        """
        self._mjcf_model.attach(mujoco_object.mjcf_obj)
        self._mujoco_objects[mujoco_object.name] = mujoco_object

    def remove(self, *, mujoco_object: MujocoObject):
        """Removes object from area-mjcf and from mujoco-object dictionary of area

        Parameters:
            mujoco_object (MujocoObject): Mujoco object to remove from area-mjcf and area-dictionary
        """
        mujoco_object.mjcf_obj.detach()
        del self._mujoco_objects[mujoco_object.name]

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
