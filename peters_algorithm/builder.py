import os
import sys
import argparse
import warnings

# Add parent folder of builder.py to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.mujoco_loader import MujocoLoader
from base.area import Area
from peters_algorithm.base.random_placer import RandomPlacer
from peters_algorithm.base.validator import Validator, MinDistanceRule
from utils.config_reader import ConfigReader
from base.border_placer import BorderPlacer
from base.environment import Environment


class Builder:
    def run(self):
        """Run peters_algorithm to create xml-file containing objects specified in config file.
        objects are given as xml by user
        """

        # assign user args to params
        args = self._get_user_args()
        config_path = args.config_path
        xml_dir = args.xml_dir

        # read config
        config = ConfigReader.execute(config_path=config_path)

        # call mujoco loader to get dictionary of mujoco objects
        mujoco_loader = MujocoLoader(config_file=config, xml_dir=xml_dir)
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
        isActive = config["Environment"]["Borders"][0]["place"]
        BorderPlacer().add(
            environment=environment,
            mujoco_object_blueprint=mujoco_objects_blueprints["Border"],
            amount=4,
            isActive=isActive,
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
        for object_settings in config["Environment"]["Objects"]:
            RandomPlacer().add(
                site=environment,
                mujoco_object_blueprint=mujoco_objects_blueprints[object_settings],
                validators=validators,
            )

        # Area Mujoco Object Placement
        for area_name, area_settings in config["Areas"].items():
            for object_name, object_settings in area_settings["Objects"].items():
                RandomPlacer().add(
                    site=area,
                    mujoco_object_blueprint=mujoco_objects_blueprints[object_name],
                    validators=validators,
                    amount=object_settings[0]["amount"],
                )

        environment.mjcf_model.attach(area.mjcf_model)
        self._to_xml(
            xml_string=environment.mjcf_model.to_xml_string(), file_name="test"
        )

        # TODO: add mujoco-object to areas with a placer

    def _get_user_args(self):
        """Read args set by user; if none are given, args are set to files and directories in "examples"

        Returns:
            args (namespace obj): Contains args set by user
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--config_path",
            help="Specify folder where yaml file is located",
            default=None,
        )
        parser.add_argument(
            "--xml_dir",
            help="Specify folder where all xml files are located",
            default=None,
        )
        args = parser.parse_args()

        if args.xml_dir is None:
            args.xml_dir = "../examples/xml_objects"
            warnings.warn(
                "xml directory not specified; running with default directory in examples"
            )
        if args.config_path is None:
            args.config_path = "../examples/config_files/simple-config.yml"
            warnings.warn(
                "config path not specified; running with default directory in examples"
            )
        return args

    def _to_xml(self, *, xml_string, file_name):
        """Exports a given string to an .xml file

        Parameters:
            xml_string (str): String that contains the environment
            file_name (str): Name of the file to be exported
        """

        with open("../export/" + file_name + ".xml", "w") as f:
            f.write(xml_string)


if __name__ == "__main__":
    builder = Builder()
    builder.run()
