from typing import Union
from dm_control import mjcf


class MujocoObject:
    """Defines a MujocoObject."""

    def __init__(
        self,
        name: str,
        mjcf_obj: mjcf.RootElement,
        obj_class: str,
        rotation: Union[tuple[float, float, float], None] = None,
        color: Union[tuple[float, float, float, float], None] = None,
        size: Union[float, None] = None,
        tags: Union[list[str], None] = None,
    ):
        """Initializes the MujocoObject class.

        Parameters:
            name (str): Specific name of object
            mjcf_obj (mjcf): Objects xml parsed into mjcf-style model of mujoco
            obj_class (str): Type of object (e.g. "Tree" or "Stone")
            rotation (tuple[float, float, float]): Rotation of object
            color (tuple[float, float, float, float]): Color rgba
            size (float): Size of ball (radius)
            tags (list(str)): User specified tags
        """
        self._name = name
        self._mjcf_obj = mjcf_obj
        self._obj_class: str = obj_class
        self._rotation = rotation
        self._color = color
        self._size = size
        self._tags = tags

    @property
    def name(self) -> str:
        """Get name.

        Returns:
            name (str): Name of the object
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set name.

        Parameters:
            name (str): Name of the object
        """
        self._name = name

    @property
    def mjcf_obj(self) -> mjcf.RootElement:
        """Get mjcf object.

        Returns:
            mjcf_obj (mjcf.RootElement): Mjcf model of the object
        """
        return self._mjcf_obj

    @mjcf_obj.setter
    def mjcf_obj(self, mjcf_obj: mjcf.RootElement) -> None:
        """Set mjcf object.

        Parameters:
            mjcf_obj (mjcf.RootElement): Mjcf model of the object
        """
        self._mjcf_obj = mjcf_obj

    @property
    def obj_class(self) -> str:
        """Get object class.

        Returns:
            obj_class (str): Object class
        """
        return self._obj_class

    @obj_class.setter
    def obj_class(self, obj_class: str) -> None:
        """Set object class.

        Parameters:
            obj_class (str): Object class
        """
        self._obj_class = obj_class

    @property
    def position(self) -> tuple[float, float, float]:
        """Get position.

        Returns:
            position (tuple[float, float, float]): Position of the object
        """
        return self._mjcf_obj.find("body", self._name.lower()).pos

    @position.setter
    def position(self, position: tuple[float, float, float]) -> None:
        """Set position.

        Parameters:
            position (tuple[float, float, float]): Position of the object
        """
        self._mjcf_obj.find("body", self._name.lower()).pos = position

    @property
    def rotation(self) -> tuple[float, float, float]:
        """Get rotation of object.

        Returns:
            rotation (tuple[float, float, float]): Rotation of object
        """
        return self._mjcf_obj.find("body", self._name.lower()).euler

    @rotation.setter
    def rotation(self, rotation: tuple[float, float, float]) -> None:
        """Set rotation of object

        Parameters:
            rotation (tuple[float, float, float]): Rotation of object
        """
        self._mjcf_obj.find("body", self._name.lower()).euler = rotation

    @property
    def color(self) -> tuple[float, float, float, float]:
        """Get color rgba.

        Returns:
            color (tuple[float, float, float, float]): color rgba
        """
        return self._mjcf_obj.find("body", self._name.lower()).geom[0].rgba

    @color.setter
    def color(self, color: tuple[float, float, float, float]) -> None:
        """Set color as rgba.

        Parameters:
            color (tuple[float, float, float, float]): color rgba
        """
        self._mjcf_obj.find("body", self._name.lower()).geom[0].rgba = color

    @property
    def size(self) -> list[float]:
        """Get size of object.

        Returns:
            size (list[float]): size of object
        """
        return self._mjcf_obj.find("body", self._name.lower()).geom[0].size

    @size.setter
    def size(self, size: list[float]) -> None:
        """Set size of object.

        Parameters:
            size (list[float]): size of object
        """
        self._mjcf_obj.find("body", self._name.lower()).geom[0].size = size

    @property
    def tags(self) -> Union[list[str], None]:
        """Get tags.

        Returns:
            tags (list[str]): Tag list of the object
        """
        return self._tags

    @tags.setter
    def tags(self, tags: list[str]) -> None:
        """Set tags.

        Parameters:
            tags (list): Tag list of the object
        """
        self._tags = tags
