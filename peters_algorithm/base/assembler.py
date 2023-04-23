import os
import sys

# Add parent folder of builder.py to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dm_control import mjcf
from peters_algorithm.base.asset_parsing.mujoco_loader import MujocoLoader
from peters_algorithm.base.world_container.area import Area
from peters_algorithm.base.asset_placement.random_placer import RandomPlacer
from peters_algorithm.base.asset_placement.validator import Validator, MinDistanceRule
from peters_algorithm.base.asset_placement.border_placer import BorderPlacer
from peters_algorithm.base.world_container.environment import Environment


class Assembler:
    """Assembles assets to corresponding world container

    Attributes
    ----------
        config (dict): config file containing user defined parameters
        xml_dir (str): string to xml-directory (containing assets)
    """
    def __init__(self, config_file: dict, xml_dir: str):
        self.config = config_file
        self.xml_dir = xml_dir

    def assemble_world(self) -> mjcf:
        """Calls the environment and areas and assembles them to create the world as and MJCF object """
        # call mujoco loader to get dictionary of mujoco objects
        mujoco_loader = MujocoLoader(config_file=self.config, xml_dir=self.xml_dir)
        mujoco_objects_blueprints = mujoco_loader.get_mujoco_objects()

        # create environment
        environment = Environment(name="Environment1", size=(10, 10, 0.1))

        # create area
        area = Area(name="Area1", size=(10, 10, 0.1))

        # Create Validators
        minDistanceValidator = Validator(
            [
                MinDistanceRule(3.0),
            ]
        )
        validators = [
            minDistanceValidator,
        ]

        # Border Placement
        # TODO: if config.environment.borders:
        has_border = self.config["Environment"]["Borders"][0]["place"]
        BorderPlacer().add(
            environment=environment,
            mujoco_object_blueprint=mujoco_objects_blueprints["Border"],
            amount=4,
            has_border=has_border,
        )

        """# Fixed Coordinate Mujoco Object Placement
        for object_name in config.environment.objects:
            if object_name.coordinates:
                FixedPlacer(environment, fixed_mujoco_object, coordinates)
                
        for area in config.areas:
            for object_name in area.objects:
                if object_name.coordinates:
                    FixedPlacer(environment, fixed_mujoco_object, coordinates)"""

        # Global Mujoco Object Placement
        for object_settings in self.config["Environment"]["Objects"]:
            RandomPlacer().add(
                site=environment,
                mujoco_object_blueprint=mujoco_objects_blueprints[object_settings],
                validators=validators,
            )

        # Area Mujoco Object Placement
        for area_name, area_settings in self.config["Areas"].items():
            for object_name, object_settings in area_settings["Objects"].items():
                RandomPlacer().add(
                    site=area,
                    mujoco_object_blueprint=mujoco_objects_blueprints[object_name],
                    validators=validators,
                    amount=object_settings[0]["amount"],
                )

        environment.mjcf_model.attach(area.mjcf_model)
        # TODO: add mujoco-object to areas with a placer

        return environment