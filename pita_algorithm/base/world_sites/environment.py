from dm_control import mjcf

from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class Environment(AbstractSite):
    """Represents the entire environment. An environment is a collection of at least one area."""

    def __init__(
        self,
        size: tuple[float, float, float],
        name: str = "Environment",
        pretty_mode: bool = False
    ):
        """Initializes the environment class.

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

        self._mujoco_objects = {}

    @property
    def name(self) -> str:
        """Get name.

        Returns:
            name (str): Name of the environment
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Set name.

        Parameters:
            name (str): Name of the environment
        """
        self._name = name

    @property
    def size(self) -> tuple[float, float, float]:
        """Get size.

        Returns:
            size (tuple[float, float, float]): Tuple defining the size of the entire environment
        """
        return self._size

    @property
    def mjcf_model(self) -> mjcf.RootElement:
        """Get mjcf model.

        Returns:
            mjcf_model (mjcf.RootElement): Mjcf model of the environment
        """
        return self._mjcf_model

    @property
    def mujoco_objects(self) -> dict:
        """Get mujoco objects.

        Returns:
            mujoco_objects (dict): Dictionary of all mujoco objects in the environment
        """
        return self._mujoco_objects

    def add(self, mujoco_object: MujocoObject):
        """Add object to the environment _mjcf_model and its mujoco-object dictionary. 
        Also sets name of object to the one given by mujoco.

        Parameters:
            mujoco_object (MujocoObject): Mujoco object to add
        """
        # The attach() method returns the attachement frame
        # i.e., a body with the attached mujoco object
        attachement_frame = self._mjcf_model.attach(mujoco_object.mjcf_obj)
        # By calling all_children() on the attachement frame, we can access their uniqe identifier
        mujoco_object.xml_id = attachement_frame.all_children()[0].full_identifier

        # Check for free joints (<joint type="free"/> or <freejoint/> but always as a direct child)
        # If present, remove it and add it again one level above
        joint_list = attachement_frame.all_children()[0].find_all(
            "joint", immediate_children_only=True
        )
        if joint_list:
            if joint_list[0].tag == "freejoint" or joint_list[0].type == "free":
                joint_attribute_dict = joint_list[0].get_attributes()
                joint_attribute_dict.pop("type", None)  # pop type key if present
                attachement_frame.add("joint", type="free", **joint_attribute_dict)
                joint_list[0].remove()

        self._mujoco_objects[mujoco_object.xml_id] = mujoco_object

    def remove(self, mujoco_object: MujocoObject):
        """Removes object from the environment _mjcf_model and its mujoco-object dictionary.

        Parameters:
            mujoco_object (MujocoObject): Tuple defining the size of the entire environment
        """
        mujoco_object.mjcf_obj.detach()
        del self._mujoco_objects[mujoco_object.xml_id]
