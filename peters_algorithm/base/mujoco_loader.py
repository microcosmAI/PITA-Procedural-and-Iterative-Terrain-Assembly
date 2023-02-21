import os.path

from peters_algorithm.utils.parser import Parser
from .mujoco_object import MujocoObject


class MujocoLoader:
    """ class to load mujoco objects as dictionary"

    Attributes:
        config_file (dict): dictionary of user defined configurations
        xml_dir (str): path to directory containing xml-file of objects
    """
    def __init__(self, *, config_file: dict, xml_dir: str):
        self.config_file = config_file
        self.xml_dir = xml_dir

    def get_mujoco_objects(self):
        """ calls class functions to get and return dictionary of mujoco-objects

        Returns:
            mujoco_dict (dict): world objects defined in config are loaded and wrapped in mujoco-object
        """
        obj_dict = self._get_object_infos()
        mujoco_dict = self._get_mujoco_dict(obj_dict)
        return mujoco_dict

    def _get_object_infos(self):
        """ handles config file structure

        Returns:
            obj_dict (dict): contains information about world objects
        """
        obj_dict = {}
        for name, params in self.config_file['Environment']['Objects'].items():
            obj_dict[name] = params

        for area, obj_in_area in self.config_file['Areas'].items():
            for name, params in self.config_file['Areas'][area]['Objects'].items():
                obj_dict[name] = params
        return obj_dict

    def _get_mujoco_dict(self, obj_dict: dict):
        """ loads xml and parses with Parser class to mjcf and combines all information to a mujoco-object

        Parameters:
            obj_dict (dict): contains information about world objects

        Returns:
            mujoco_dict (dict): dictionary of world objects as mujoco-objects
        """
        mujoco_dict = {}
        for obj, params in obj_dict.items():
            obj_xml_path = os.path.join(self.xml_dir, obj + ".xml")
            mjcf = Parser.get_mjcf(xml_path=obj_xml_path)
            obj_type, attachable = self._read_params(params)
            mujoco_obj = MujocoObject(name=obj, mjcf_obj=mjcf, obj_type=obj_type, attachable=attachable)
            mujoco_dict[obj] = mujoco_obj
        return mujoco_dict

    @staticmethod
    def _read_params(params: list):
        """ helper function to read object specific parameters set in config file

        Parameters:
            params (list(dict)): list of world object specific parameters given as dictionary

        Returns:
            obj_type (str): type of world-object; relates to mujoco-object parameter
            attachable (bool): True if object can be attached to a container-type object; relates to mujoco-object parameter
        """
        obj_type = None
        attachable = None
        if not params == None:
            for dict_ in params:
                if "type" in dict_.keys():
                    obj_type = dict_["type"]
                if "attachable" in dict_.keys():
                    attachable = dict_["attachable"]
        return obj_type, attachable
