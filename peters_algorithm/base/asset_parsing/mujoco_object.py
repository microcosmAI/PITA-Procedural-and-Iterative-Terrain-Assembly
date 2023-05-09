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
        colors: tuple[float, float, float, float] = None,
        sizes: tuple[float, float, float] = None,
    ):
        """Initializes the MujocoObject class
        ToDo: doc
        Parameters:
            name (str): Specific name of object
            container (bool): Set to true if the object is a container; it can store another item (e.g. tree with container for an apple)
            type (str): Type of object (e.g. "tree" or "stone")
            mjcf_object (mjcf): Objects xml parsed into mjcf-style model of mujoco
            coordinates (tuple): Coordinates of the object
        """
        self._name: str = name
        self._mjcf_obj: mjcf.RootElement = mjcf_obj
        self._obj_type: str = obj_type
        self._attachable: bool = attachable
        self._coordinates: tuple = coordinates
        self._colors: tuple = colors
        self._sizes: tuple = sizes

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
    def colors(self) -> tuple[float, float, float, float]:
        """Get amount of colors as range

        Returns:
            colors (tuple[int, int]): amount of colors given as range
        """
        # ToDo: aus mjcf holen
        return self._colors

    @colors.setter
    def colors(self, colors: tuple[float, float, float, float]):
        """Set colors as range"""
        self._colors = colors
        # ToDo: in mjcf ändern

    @property
    def sizes(self) -> tuple[float, float, float]:
        """Get sizes as range

        Returns:
            sizes (tuple[int, int]): sizes given as range
        """
        # ToDo: aus mjcf holen
        return self._sizes

    @sizes.setter
    def sizes(self, sizes: tuple[float, float, float]):
        """Set sizes as range"""
        # ToDo: in mjcf ändern
        self._sizes = sizes
