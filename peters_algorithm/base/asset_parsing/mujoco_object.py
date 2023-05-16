from dm_control import mjcf


class MujocoObject:
    """Class to define a MujocoObject"""

    def __init__(
        self,
        name: str,
        mjcf_obj: mjcf.RootElement,
        obj_type: str,
        attachable: bool,
        coordinates: tuple[float, float, float] = None,
        color: tuple[float, float, float, float] = None,
        size: float = None,
    ):
        """Initializes the MujocoObject class

        Parameters:
            name (str): Specific name of object
            mjcf_obj (mjcf): Objects xml parsed into mjcf-style model of mujoco
            obj_type (str): Type of object (e.g. "tree" or "stone")
            attachable (bool): decides if object is attachable
            coordinates (tuple): Coordinates of the object
            color (tuple[float, float, float, float]): color rgba
            size (float): size of ball (radius)
        """
        self._name: str = name
        self._mjcf_obj: mjcf.RootElement = mjcf_obj
        self._obj_type: str = obj_type
        self._attachable: bool = attachable
        self._coordinates: tuple = coordinates
        self._color: tuple = color
        self._size: float = size

    @property
    def name(self) -> str:
        """Get name

        Returns:
            name (str): Name of the object
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Set name"""
        self._name = name

    @property
    def mjcf_obj(self) -> mjcf.RootElement:
        """Get mjcf object

        Returns:
            mjcf_obj (mjcf): Mjcf model of the object
        """
        return self._mjcf_obj

    @mjcf_obj.setter
    def mjcf_obj(self, mjcf_obj: mjcf.RootElement):
        """Set mjcf object"""
        self._mjcf_obj = mjcf_obj

    @property
    def obj_type(self) -> str:
        """Get object type

        Returns:
            obj_type (str): Type of the object
        """
        return self._obj_type

    @obj_type.setter
    def obj_type(self, obj_type: str):
        """Set object type"""
        self._obj_type = obj_type

    @property
    def attachable(self) -> bool:
        """Get attachable

        Returns:
            attachable (bool): True if object is attachable, False otherwise
        """
        return self._attachable

    @attachable.setter
    def attachable(self, attachable: bool):
        """Set attachable"""
        self._attachable = attachable

    @property
    def position(self) -> tuple[float, float, float]:
        """Get position

        Returns:
            position (tuple): Position of the object
        """
        return self._mjcf_obj.find("body", self._name.lower()).pos

    @position.setter
    def position(self, position: tuple[float, float, float]):
        """Set position"""
        self._mjcf_obj.find("body", self._name.lower()).pos = position

    @property
    def color(self) -> tuple[float, float, float, float]:
        """Get color rgba

        Returns:
            color (tuple[float, float, float, float]): color rgba
        """
        return self._mjcf_obj.find("body", self._name.lower()).geom[0].rgba

    @color.setter
    def color(self, color: tuple[float, float, float, float]):
        """Set color as rgba"""
        self._mjcf_obj.find("body", self._name.lower()).geom[0].rgba = color

    @property
    def size(self) -> float:
        """Get size of object

        Returns:
            size (float): size of object
        """
        return self._mjcf_obj.find("body", self._name.lower()).geom[0].size

    @size.setter
    def size(self, size: float):
        """Set size of object"""
        mjcf_pos = self.position
        mjcf_pos[2] = size
        self.position = mjcf_pos
        self._mjcf_obj.find("body", self._name.lower()).geom[0].size = [size]
