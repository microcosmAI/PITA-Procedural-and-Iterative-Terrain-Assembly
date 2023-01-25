import argparse
import warnings

from parser import Parser


class Builder:

    def run(self):
        """ run s.peters_algorithm to create xml-file containing objects specified in config file.
            objects are given as xml by user
        """

        # assign user args to params
        args = self._get_user_args()
        config_path = args.config_path
        xml_dir = args.xml_dir

        # call Parser class to read given config file and get mjcf-objects in given directory
        parser = Parser(config_path=config_path, xml_dir=xml_dir)
        config_file, mjcfs = parser.execute()

        # ToDo: init environment

        # ToDo: LayoutManager

        # ToDo: init areas

        # ToDo: add mujoco-object to areas; objects from parser

    def _get_user_args(self):
        """ read args set by user; if none are given, args are set to files and directories in "examples" """

        parser = argparse.ArgumentParser()
        parser.add_argument("--config_path", help="Specify folder where yaml file is located",
                            default=None)
        parser.add_argument("--xml_dir", help="Specify folder where all xml files are located",
                            default=None)
        args = parser.parse_args()

        if args.xml_dir is None:
            args.xml_dir = "./examples/xml_objects"
            warnings.warn("xml directory not specified; running with default directory in examples")
        if args.config_path is None:
            args.config_path = "./examples/config_files/simple-config.yml"
            warnings.warn("config path not specified; running with default directory in examples")

        return args

    def _to_xml(self):
        """ combine MJCFs to single xml-file """
        pass


if __name__ == "__main__":
    builder = Builder()
    builder.run()
