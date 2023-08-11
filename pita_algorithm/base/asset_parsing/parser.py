import os
import logging
from dm_control import mjcf


class Parser:
    """Class to parse xml-file in given path to mujoco's MJCF-object."""

    @staticmethod
    def get_mjcf(xml_path: str) -> mjcf.RootElement:
        """Parses xml-file to MJCF-object.

        Parameters:
            xml_path (str): Path to xml-file

        Returns:
            mjcf_obj (mjcf.RootElement): Mjcf object of given xml-file
        """
        logger = logging.getLogger()
        if xml_path is None:
            logger.error("No xml file provided.")
            raise ValueError("No xml file provided.")
        if not os.path.isfile(xml_path):
            logger.error(f"Could not find xml path '{xml_path}'.")
            raise ValueError(f"Could not find xml path '{xml_path}'.")

        mjcf_obj = mjcf.from_path(xml_path)

        return mjcf_obj
