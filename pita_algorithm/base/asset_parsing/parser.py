import os
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
        if xml_path is None:
            raise ValueError("No xml file provided")
        if not os.path.isfile(xml_path):
            raise ValueError("Could not find xml path provided")

        mjcf_obj = mjcf.from_path(xml_path)
        
        return mjcf_obj
