import os 
import sys
import argparse
import warnings

# Add parent folder of builder.py to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.mujoco_loader import MujocoLoader
from base.area import Area
from utils.config_reader import ConfigReader
from base.border_placer import BorderPlacer

from base.environment import Environment

class Builder:

    def run(self):
        """ run peters_algorithm to create xml-file containing objects specified in config file.
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

        # exmaple on how to cretae an area and add and remove an object based on a mujoco-object
        # Note: placer class will handle further details (e.g. amount of trees etc)
        area = Area(name="Area1", size=(10, 10))
        area.add(mujoco_object=mujoco_objects_blueprints["Tree"])
        area.remove(mujoco_object=mujoco_objects_blueprints["Tree"])

        BorderPlacer().add(environment=environment, mujoco_object_blueprint=mujoco_objects_blueprints["Border"], amount=4)

        self._to_xml(xml_string=environment.mjcf_model.to_xml_string(), file_name="test")

        # ToDo: init environment

        # ToDo: add mujoco-object to areas with a placer

    def _get_user_args(self):
        """ read args set by user; if none are given, args are set to files and directories in "examples"

        Returns:
            args (namespace obj): contains args set by user
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("--config_path", help="Specify folder where yaml file is located",
                            default=None)
        parser.add_argument("--xml_dir", help="Specify folder where all xml files are located",
                            default=None)
        args = parser.parse_args()

        if args.xml_dir is None:
            args.xml_dir = "../examples/xml_objects"
            warnings.warn("xml directory not specified; running with default directory in examples")
        if args.config_path is None:
            args.config_path = "../examples/config_files/simple-config.yml"
            warnings.warn("config path not specified; running with default directory in examples")
        return args

    def _to_xml(self, *, xml_string, file_name):
        """ Exports a given string to an .xml file """
        
        with open("../export/" + file_name + ".xml", "w") as f:
            f.write(xml_string)


if __name__ == "__main__":
    builder = Builder()
    builder.run()
