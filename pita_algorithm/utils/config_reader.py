import os
import yaml
import logging


class ConfigReader:
    """Reads yaml-file containing user defined configurations."""

    @staticmethod
    def execute(config_path: str) -> dict:
        """Reads yaml-config file.

        Parameters:
            config_path (str): Path to yaml-config file

        Returns:
            config (dict): Dictionary of user defined configurations
        """
        logger = logging.getLogger()
        if config_path is None:
            logger.error("No config file provided.")
            raise ValueError("No config file provided.")
        if not os.path.isfile(config_path):
            logger.info(f"Config path: {config_path}")
            logger.error("Could not find config file in path provided.")
            raise ValueError(f"Could not find config file in path '{config_path}'.")

        stream = open(config_path, "r")
        config = yaml.load(stream, Loader=yaml.SafeLoader)

        return config
