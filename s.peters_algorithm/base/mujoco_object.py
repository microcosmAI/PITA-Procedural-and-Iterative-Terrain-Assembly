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

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_container(self):
        return self.container

    def set_container(self, container):
        self.container = container

    def get_obj_type(self):
        return self.obj_type

    def set_type(self, obj_type):
        self.obj_type = obj_type

    def get_mjcf_obj(self):
        return self.mjcf_obj

    def set_mjcf_obj(self, mjcf_obj):
        self.mjcf_obj = mjcf_obj
