from .site import Site
from dm_control import mjcf
from .mujoco_object import MujocoObject


class Area(Site):
    """ area object class

    Attributes:
        name (str): name of area
        size (tuple): size of area
        mjcf_model (mjcf): mjcf model of area
        mujoco_objects (dict(mujoco_objects)): contains objects in area as mujoco-objects
    """
    def __init__(self, *, name: str, size: tuple):
        self._name = name
        self._size = size
        self._mjcf_model = self._initialize_area()
        self._mujoco_objects = {}

    def _initialize_area(self):
        """ initialize area

        Returns:
            mjcf_model (mjcf): mjcf-object of area
        """
        self._mjcf_model = mjcf.RootElement(model=self.name)
        self._mjcf_model.worldbody.add("geom", name="base_plane_area", type="plane",
                                       size=self._size)
        return self._mjcf_model

    def add(self, *, mujoco_object: MujocoObject):
        """ add object to area-mjcf and to mujoco-object dictionary of area

        Parameters:
            mujoco_object (MujocoObject): mujoco object to add to area-mjcf and area-dictionary
        """
        self._mjcf_model.attach(mujoco_object.mjcf_obj)
        self._mujoco_objects[mujoco_object.name] = mujoco_object

    def remove(self, *, mujoco_object: MujocoObject):
        """ removes object from area-mjcf and from mujoco-object dictionary of area

        Parameters:
            mujoco_object (MujocoObject): mujoco object to remove from area-mjcf and area-dictionary
        """
        mujoco_object.mjcf_obj.detach()
        del self._mujoco_objects[mujoco_object.name]

    @property
    def name(self):
        """ get name """
        return self._name

    @name.setter
    def name(self, name: str):
        """ set name """
        self._name = name

    @property
    def size(self):
        """ get size """
        return self._size

    @property
    def mjcf_model(self):
        """ get mjcf_model """
        return self._mjcf_model

    @property
    def mujoco_objects(self):
        """ get mujoco_objects """
        return self._mujoco_objects
