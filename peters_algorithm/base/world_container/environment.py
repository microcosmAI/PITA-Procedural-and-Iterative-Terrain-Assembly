from dm_control import mjcf

from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from peters_algorithm.base.world_container.abstract_container import AbstractContainer


class Environment(AbstractContainer):
    """Class that represents the entire environment"""

    def __init__(
        self,
        *,
        size: tuple[float, float, float],
        name: str = "Environment",
        pretty_mode: bool = False
    ):
        """Initializes the environment class

        Parameters:
            size (tuple): Tuple defining the size of the entire environment (length, width, height)
            name (str): Name of the environment
            pretty_style (bool): If true, the environment will be created with a pretty style
        """
        self._size = size
        self._name = name
        self._mjcf_model = mjcf.RootElement()

        if pretty_mode:
            self._mjcf_model.asset.add(
                "texture",
                type="skybox",
                builtin="gradient",
                rgb1="0. .82 1.",
                rgb2=".035 .337 .475",
                width="512",
                height="512",
            )
            self._mjcf_model.asset.add(
                "texture",
                name="grid",
                type="2d",
                builtin="checker",
                rgb1=".1 .2 .3",
                rgb2=".2 .3 .4",
                width="300",
                height="300",
                mark="edge",
                markrgb=".2 .3 .4",
            )
            self._mjcf_model.asset.add(
                "material",
                name="grid",
                texture="grid",
                texrepeat="1 1",
                texuniform="true",
                reflectance=".2",
            )
            self._mjcf_model.worldbody.add(
                "geom", name="base_plane", type="plane", size=size, material="grid"
            )
        else:
            self._mjcf_model.worldbody.add(
                "geom", name="base_plane", type="plane", size=size
            )
        self._mujoco_objects = {}

    @property
    def name(self):
        """Get name

        Returns:
            name (str): Name of the environment
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Set name

        Parameters:
            name (str): Name of the environment
        """
        self._name = name

    @property
    def size(self):
        """Get size

        Returns:
            size (tuple): Tuple defining the size of the entire environment
        """
        return self._size

    @property
    def mjcf_model(self):
        """Get mjcf model

        Returns:
            mjcf_model (mjcf): Mjcf model of the environment
        """
        return self._mjcf_model

    @property
    def mujoco_objects(self):
        """Get mujoco objects

        Returns:
            mujoco_objects (dict): Dictionary of all mujoco objects in the environment
        """
        return self._mujoco_objects

    def add(self, *, mujoco_object: MujocoObject):
        """Adds a mujoco object

        Parameters:
            mujoco_object (MujocoObject): Tuple defining the size of the entire environment
        """
        self._mjcf_model.attach(mujoco_object.mjcf_obj)
        self._mujoco_objects[mujoco_object.name] = mujoco_object

    def remove(self, *, mujoco_object: MujocoObject):
        """Removes a given mujoco object

        Parameters:
            mujoco_object (MujocoObject): Tuple defining the size of the entire environment
        """
        mujoco_object.mjcf_obj.detach()
        del self._mujoco_objects[mujoco_object.name]
