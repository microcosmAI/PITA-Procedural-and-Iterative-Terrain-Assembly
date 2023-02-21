from dm_control import mjcf


class MujocoObject:
    """ class to define a MujocoObject

    Attributes:
        name (str): specific name of object
        container (bool): set to true if the object is a container; it can store another item (e.g. tree with container for an apple)
        type (str): type of object (e.g. "tree" or "stone")
        mjcf_object (mjcf): objects xml parsed into mjcf-style model of mujoco
    """

    def __init__(self, name: str, mjcf_obj: mjcf, obj_type: str, attachable: bool):
        self._name: str = name
        self._mjcf_obj: mjcf.RootElement = mjcf_obj
        self._obj_type: str = obj_type
        self._attachable: bool = attachable

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def mjcf_obj(self) -> mjcf.RootElement:
        return self._mjcf_obj

    @mjcf_obj.setter
    def mjcf_obj(self, mjcf_obj: mjcf.RootElement):
        self._mjcf_obj = mjcf_obj

    @property
    def obj_type(self) -> str:
        return self._obj_type

    @obj_type.setter
    def obj_type(self, obj_type: str):
        self._obj_type = obj_type

    @property
    def attachable(self) -> bool:
        return self._attachable

    @attachable.setter
    def attachable(self, attachable: bool):
        self._attachable = attachable

    @property
    def position(self) -> tuple[float, float, float]:
        return self._mjcf_obj.find("body", self._name.lower()).pos

    @position.setter
    def position(self, position: tuple[float, float, float]):
        self._mjcf_obj.find("body", self._name.lower()).pos = position
