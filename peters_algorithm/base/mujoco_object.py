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
    def __init__(self, name: str, mjcf_obj: mjcf, obj_type: str, attachable: bool):
        self._name = name
        self._mjcf_obj = mjcf_obj
        self._obj_type = obj_type
        self._attachable = attachable

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def mjcf_obj(self):
        return self._mjcf_obj

    @mjcf_obj.setter
    def mjcf_obj(self, mjcf_obj):
        self._mjcf_obj = mjcf_obj

    @property
    def obj_type(self):
        return self._obj_type

    @obj_type.setter
    def obj_type(self, obj_type):
        self._obj_type = obj_type

    @property
    def attachable(self):
        return self._attachable

    @attachable.setter
    def attachable(self, attachable):
        self._attachable = attachable
