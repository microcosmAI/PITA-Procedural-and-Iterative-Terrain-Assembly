import os
import sys
import random
import argparse
import warnings
import numpy as np
from typing import Union

# Add parent folder of builder.py to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pita_algorithm.base.assembler import Assembler
from pita_algorithm.utils.json_exporter import JSONExporter
from pita_algorithm.utils.xml_exporter import XMLExporter
from pita_algorithm.utils.config_reader import ConfigReader


class PITA:
    """Main class to run the PITA algorithm."""

    def run(
        self,
        random_seed: Union[int, None] = None,
        config_path: Union[str, None] = None,
        xml_dir: Union[str, None] = None,
        export_path: Union[str, None] = None,
    ):
        """Run pita_algorithm to create xml-file containing objects specified in config file.
        Objects are given as xml by the user.

        Parameters:
            random_seed (Union[int, None]): Seed for reproducibility
            config_path (Union[str, None]): Path to where the yaml file is located
            xml_dir (Union[str, None]): Folder where all xml files are located
            export_path (Union[str, None]): Path (including file name but excluding extension) to export to
        """
        if config_path is None:
            config_path = "examples/config_files/simple-config.yml"
            warnings.warn(
                "config path not specified; running with default directory in examples"
            )
        if xml_dir is None:
            xml_dir = "examples/xml_objects"
            warnings.warn(
                "xml directory not specified; running with default directory in examples"
            )
        if export_path is None:
            export_path = "export/test"
            warnings.warn(
                "export path not specified; running with default directory in export and filename 'test'"
            )

        # Read config file and assemble environment and export to xml and json
        config = ConfigReader.execute(config_path=config_path)

        # Set random seed
        if (
            random_seed is not None
            and "random_seed" in config["Environment"]
            and config["Environment"]["random_seed"] is not None
        ):
            print(
                "Two seeds were specified (call argument to PITA.run() and in level config file). Using seed from the call."
            )
            print(f"Setting random seed to {random_seed}")
            np.random.seed(random_seed)
            random.seed(random_seed)
        elif random_seed is not None:
            print(f"Setting random seed to {random_seed}")
            np.random.seed(random_seed)
            random.seed(random_seed)
        elif (
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
        XMLExporter.to_xml(
            xml_string=environment.mjcf_model.to_xml_string(),
            export_path=export_path,
        )
        JSONExporter.export(
            export_path=export_path,
            config=config,
            environment=environment,
            areas=areas,
        )


if __name__ == "__main__":
    PITA().run()
