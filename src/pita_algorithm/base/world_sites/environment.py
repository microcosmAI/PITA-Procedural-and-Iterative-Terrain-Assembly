import logging
import numpy as np
from dm_control import mjcf

from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class Environment(AbstractSite):
    """Represents the entire environment. An environment is a collection of at least one area."""

    def __init__(
        self,
        size: tuple[float, float, float],
        name: str = "Environment",
        pretty_mode: bool = False,
        headlight: dict = None,
    ):
        """Constructor of the Environment class.

        Parameters:
            size (tuple): Tuple defining the size of the entire environment (length, width, height)
            name (str): Name of the environment
            pretty_style (bool): If true, the environment will be created with a pretty style
            headlight (dict): Dictionary containing parameters for the mujoco headlight
        """
        self._size = self.calculate_size(size)
        self._name = name
        self._mjcf_model = mjcf.RootElement()

        # apply params for visuals
        if headlight:
            for param in headlight:
                for key, value in param.items():
                    setattr(self._mjcf_model.visual.headlight, key, value)

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
        self._mujoco_objects: dict[str, MujocoObject] = {}

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
    def size(self) -> list:
        """Get size.

        Returns:
            size (list): Tuple defining the size of the entire environment
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
        # The attach() method returns the attachment frame
        # i.e., a body with the attached mujoco object
        attachment_frame = self._mjcf_model.attach(mujoco_object.mjcf_obj)
        # By calling all_children() on the attachment frame, we can access their unique identifier
        mujoco_object.xml_id = attachment_frame.all_children()[0].full_identifier

        # Check for free joints (<joint type="free"/> or <freejoint/> but always as a direct child)
        # If present, remove it and add it again one level above
        joint_list = attachment_frame.all_children()[0].find_all(
            "joint", immediate_children_only=True
        )
        if joint_list:
            if joint_list[0].tag == "freejoint" or joint_list[0].type == "free":
                joint_attribute_dict = joint_list[0].get_attributes()
                joint_attribute_dict.pop("type", None)  # pop type key if present
                attachment_frame.add("joint", type="free", **joint_attribute_dict)
                joint_list[0].remove()

                # Fix rotation bug, i.e., move euler value into the parent body (attachment_frame) and reset it in the mujoco_object
                # For the environment dynamics to work properly (adding the agent's rotation to qvel would otherwise not be possible)
                attachment_frame.euler = mujoco_object.rotation
                mujoco_object.rotation = (0.0, 0.0, 0.0)

        self._mujoco_objects[mujoco_object.xml_id] = mujoco_object

    def remove(self, mujoco_object: MujocoObject):
        """Removes object from the environment _mjcf_model and its mujoco-object dictionary.

        Parameters:
            mujoco_object (MujocoObject): Tuple defining the size of the entire environment
        """
        mujoco_object.mjcf_obj.detach()
        del self._mujoco_objects[mujoco_object.xml_id]

    def calculate_size(self, size_range: tuple) -> list:
        """Calculates the size of the environment with a given size_range (can be many different types).

        Parameters:
            size_range (tuple): Tuple defining the size range of the environment (length, width, height)

        Returns:
            size (list): Tuple defining the size of the entire environment
        """
        logger = logging.getLogger()

        if size_range[0] is None:
            logger.error(
                "No size range provided for environment. Use keyword 'size_range' in config file."
            )
            raise ValueError(
                "No size range provided for environment. Use keyword 'size_range' in config file."
            )

        if isinstance(size_range[0][0], (float, int)):
            size = (
                list(
                    np.random.uniform(
                        low=size_range[0][0], high=size_range[0][1], size=1
                    )
                )
                * 2
            )

        else:
            # Drop outer tuple and list and merge dictionaries
            size_range_dict = {
                key: value
                for dictionary in size_range[0]
                for key, value in dictionary.items()
            }

            if not {"length_range", "width_range"}.issubset(
                set(size_range_dict.keys())
            ):
                logger.error(
                    "Both length_range and width_range must be specified for environment if environment size "
                    "should be randomized in given ranges."
                )
                raise ValueError(
                    "Both length_range and width_range must be specified for environment if environment "
                    "size should be randomized in given ranges."
                )

            else:
                size = []
                size.extend(
                    np.random.uniform(
                        low=size_range_dict["length_range"][0],
                        high=size_range_dict["length_range"][1],
                        size=1,
                    )
                )
                size.extend(
                    np.random.uniform(
                        low=size_range_dict["width_range"][0],
                        high=size_range_dict["width_range"][1],
                        size=1,
                    )
                )
        size = [
            (x / 2) for x in size
        ]  # because mujoco transforms size to ([-size_x, size_x], [-size_y, size_y])
        return size
