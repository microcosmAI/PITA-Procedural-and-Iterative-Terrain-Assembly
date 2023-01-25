import argparse
import warnings

from parser import Parser


class Builder:

    @staticmethod
    def run():
        """ run s.peters_algorithm to create xml-file containing objects specified in config file.
            objects are given as xml by user
        """

        # read args set by user
        parser = argparse.ArgumentParser()
        parser.add_argument("--config_path", help="Specify folder where yaml file is located",
                            default=None)
        parser.add_argument("--xml_dir", help="Specify folder where all xml files are located",
                            default=None)
        args = parser.parse_args()
        config_path = args.config_path
        xml_dir = args.xml_dir

        if xml_dir is None:
            xml_dir = "./examples/xml_objects"
            warnings.warn("xml directory not specified; running with default directory in examples")
        if config_path is None:
            config_path = "./examples/config_files/simple-config.yml"
            warnings.warn("config path not specified; running with default directory in examples")

        # call Parser class to read given config file and get mjcf-objects in given directory
        parser = Parser(config_path=config_path, xml_dir=xml_dir)
        config_file, mjcfs = parser.execute()

        # ToDo: init environment

        # ToDo: LayoutManager

        # ToDo: init areas

        # ToDo: add mujoco-object to areas; objects from parser

    def _to_xml(self):
        """ combine MJCFs to single xml-file """
        pass


if __name__ == "__main__":
    Builder.run()
