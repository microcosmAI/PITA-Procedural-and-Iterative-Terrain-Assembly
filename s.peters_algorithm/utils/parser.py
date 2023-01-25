import os

from dm_control import mjcf


class Parser:
    """ class to parse xml-files in given directory to mujoco's MJCF-objects

    ToDo: change loading of whole directory to specific xml-files needed (defined in config)

    Attributes:
    ----------
    xml_dir: str
        path to directory containing xml-files
    """
    def __init__(self, *, xml_dir: str = "../examples/humanoid.xml"):
        self.xml_dir = xml_dir

    def get_mjcfs(self):
        """ executes config reader function and parses xml-files to MJCF-objects

        Returns:
        -------
        config: dict
            dictionary of yaml-config file entries
        mjcfs: list
            contains list of mjcf-objects, parsed from xml-files in given directory
        """

        mjcfs = self._obj_from_xml_to_mjcf()
        return mjcfs

    def _obj_from_xml_to_mjcf(self):
        """ parses xml-files in given directory to mujoco's mjcf-objects

        ToDo: on specific load of xml-file ond not whole dir, also adjust error-capturing conditions

        Returns:
        -------
        mjcfs: list
            contains list of mjcf-objects, parsed from xml-files in given directory
        """
        if self.xml_dir is None:
            raise ValueError("No xml directory provided")
        if not os.path.isdir(self.xml_dir):
            raise ValueError("Could not find xml directory provided")

        files_in_dir = os.listdir(self.xml_dir)
        mjcfs = list()
        for file in files_in_dir:
            mjcf_model = mjcf.from_path(os.path.join(self.xml_dir, file))
            mjcfs.append(mjcf_model)
        return mjcfs
