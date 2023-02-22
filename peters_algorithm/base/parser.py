import os

from dm_control import mjcf


class Parser:
    """Class to parse xml-files in given directory to mujoco's MJCF-objects

    TODO: change loading of whole directory to specific xml-files needed (defined in config)

    Parameters:
        xml_dir (str): Path to directory containing xml-files
    """

    def __init__(self, *, xml_dir: str = "../examples/humanoid.xml"):
        self.xml_dir = xml_dir

    def get_mjcfs(self):
        """Executes config reader function and parses xml-files to MJCF-objects

        Returns:
            config (dict): Dictionary of yaml-config file entries
            mjcfs (list): Contains list of mjcf-objects, parsed from xml-files in given directory
        """
        mjcfs = self._obj_from_xml_to_mjcf()
        return mjcfs

    def _obj_from_xml_to_mjcf(self):
        """Parses xml-files in given directory to mujoco's mjcf-objects

        TODO: on specific load of xml-file ond not whole dir, also adjust error-capturing conditions

        Returns:
            mjcfs (list): Contains list of mjcf-objects, parsed from xml-files in given directory
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
