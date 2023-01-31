import os

from dm_control import mjcf


class Parser:
    """ class to parse xml-file in given path to mujoco's MJCF-object """

    @staticmethod
    def get_mjcf(*, xml_path: str):
        """ parses xml-file to MJCF-object

        Returns:
            mjcf_ (mjcf): mjcf object of given xml-file
        """
        if xml_path is None:
            raise ValueError("No xml file provided")
        if not os.path.isfile(xml_path):
            raise ValueError("Could not find xml path provided")

        mjcf_ = mjcf.from_path(xml_path)
        return mjcf_
