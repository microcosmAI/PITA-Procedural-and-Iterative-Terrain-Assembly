from pitapy.base.asset_parsing.mujoco_object import MujocoObject
from pitapy.base.asset_parsing.mujoco_loader import MujocoLoader


class BlueprintManager:
    """Creates and manages the Mujoco objects blueprints."""

    def __init__(self, config: dict, xml_dir: str):
        """Constructor of the BlueprintManager class.

        Parameters:
            config (dict): Configuration dictionary
            xml_dir (str): Path to the xml files
        """
        self.config: dict = config
        self.xml_dir: str = xml_dir
        self.mujoco_objects_blueprints: dict[str, MujocoObject] = {}

    def get_object_blueprints(self) -> (dict, dict):
        """Creates and manipulates the mujoco objects blueprints.

        Returns:
            (dict, dict): Dictionaries of mujoco objects blueprints and mujoco objects rule blueprints
        """
        mujoco_loader = MujocoLoader(config_file=self.config, xml_dir=self.xml_dir)
        self.mujoco_objects_blueprints = mujoco_loader.get_mujoco_objects()
        return self.mujoco_objects_blueprints
