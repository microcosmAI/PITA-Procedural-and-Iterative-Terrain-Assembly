import os
import sys
import random
import argparse
import warnings
import numpy as np

# Add parent folder of builder.py to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pita_algorithm.base.assembler import Assembler
from pita_algorithm.utils.json_exporter import JSONExporter
from pita_algorithm.utils.config_reader import ConfigReader


class PITA:
    """Main class to run the PITA algorithm."""

    def run(self):
        """Run pita_algorithm to create xml-file containing objects specified in config file.
        Objects are given as xml by the user.
        """
        # Assign user args to params
        args = self._get_user_args()
        config_path = args.config_path
        xml_dir = args.xml_dir

        # Read config file and assemble environment and export to xml and json
        config = ConfigReader.execute(config_path=config_path)

        # Set Random Seed
        if (
            "random_seed" in config["Environment"]
            and config["Environment"]["random_seed"] is not None
        ):
            random_seed = config["Environment"]["random_seed"]
            print(f"Setting random seed to {random_seed}")
            np.random.seed(random_seed)
            random.seed(random_seed)

        environment, areas = Assembler(
            config_file=config, xml_dir=xml_dir
        ).assemble_world()
        self._to_xml(
            xml_string=environment.mjcf_model.to_xml_string(), file_name="test"
        )
        JSONExporter.export(
            filename="environment_configuration",
            config=config,
            environment=environment,
            areas=areas,
        )

    def _get_user_args(self) -> argparse.Namespace:
        """Read args defined by user. If none are given, args are set to files and
        directories in the 'examples' folder.

        Returns:
            args (argparse.Namespace): Contains args defined by user
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
            args.xml_dir = "examples/xml_objects"
            warnings.warn(
                "xml directory not specified; running with default directory in examples"
            )
        if args.config_path is None:
            args.config_path = "examples/config_files/simple-config.yml"
            warnings.warn(
                "config path not specified; running with default directory in examples"
            )
        return args

    def _to_xml(self, xml_string, file_name):
        """Exports a given string to an .xml file.

        Parameters:
            xml_string (str): String representation of the environment mjcf model
            file_name (str): Name of the file to be exported
        """
        with open("export/" + file_name + ".xml", "w") as f:
            f.write(xml_string)


if __name__ == "__main__":
    PITA().run()
