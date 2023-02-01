import os
import yaml


class ConfigReader:
    """ class to read yaml-file (containing configurations)
    """

    @staticmethod
    def execute(*, config_path: str):
        """ reads yaml-config file

        Parameters:
            config_path (str): path to yaml-config file

        Returns:
            config (dict): dictionary of user defined configurations
        """
        if config_path is None:
            raise ValueError("No config file provided")
        if not os.path.isfile(config_path):
            raise ValueError("Could not find config file in path provided")

        stream = open(config_path, 'r')
        config = yaml.load(stream, Loader=yaml.SafeLoader)
        return config
