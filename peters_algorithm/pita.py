import os
import argparse
import warnings

from peters_algorithm.base.assembler import Assembler
from peters_algorithm.utils.config_reader import ConfigReader


class PetersAlgorithm:
    """Main class to run stochastic world generation for ReinforcementLearning applications"""

    def run(self):
        """Run peters_algorithm to create xml-file containing objects specified in config file.
        objects are given as xml by user
        """
        # assign user args to params
        args = self._get_user_args()
        config_path = args.config_path
        xml_dir = args.xml_dir

        config = ConfigReader.execute(config_path=config_path)
        environment = Assembler(config_file=config, xml_dir=xml_dir).assemble_world()
        self._to_xml(
            xml_string=environment.mjcf_model.to_xml_string(), file_name="test"
        )

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
    PetersAlgorithm().run()
