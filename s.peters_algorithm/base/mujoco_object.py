from dm_control import mjcf


class MujocoObject:
    """ class to define a MujocoObject

    Attributes:
    ----------
    name: str
        specific name of object
    container: bool
        set to true if the object is a container; it can store another item (e.g. tree with container for an apple)
    type: str
        type of object (e.g. "tree" or "stone")
    mjcf_object: mjcf
        objects xml parsed into mjcf-style model of mujoco
    """
    def __init__(self, name: str, container: bool, obj_type: str, mjcf_obj: mjcf):
        self.name = name
        self.container = container
        self.obj_type = obj_type
        self.mjcf_obj = mjcf_obj

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name

    @property
    def container(self):
        return self.container

    @container.setter
    def container(self, container):
        self.container = container

    @property
    def obj_type(self):
        return self.obj_type

    @obj_type.setter
    def obj_type(self, obj_type):
        self.obj_type = obj_type

    @property
    def mjcf_obj(self):
        return self.mjcf_obj

    @mjcf_obj.setter
    def mjcf_obj(self, mjcf_obj):
        self.mjcf_obj = mjcf_obj
