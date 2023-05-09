import os.path
import numpy as np
from peters_algorithm.base.asset_parsing.parser import Parser
from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class MujocoLoader:
    """Class to load mujoco objects as dictionary"""

    def __init__(self, *, config_file: dict, xml_dir: str):
        """Initializes MujocoLoader class

        Parameters:
            config_file (dict): Dictionary of user defined configurations
            xml_dir (str): Path to directory containing xml-file of objects
        """
        self.config_file = config_file
        self.xml_dir = xml_dir

    def get_mujoco_objects(self):
        """Calls class functions to get and return dictionary of mujoco-objects

        Returns:
            mujoco_dict (dict): World objects defined in config are loaded and wrapped in mujoco-object
        """
        obj_dict = self._get_object_infos()
        mujoco_dict = self._get_mujoco_dict(obj_dict)
        return mujoco_dict

    def _get_object_infos(self):
        """Handles config file structure

        Returns:
            obj_dict (dict): Contains information about world_container objects
        """
        obj_dict = {}

        for name, params in self.config_file["Environment"].items():
            if name == "Borders":
                name = "Border"  # possible type of border
                obj_dict[name] = params

        for name, params in self.config_file["Environment"]["Objects"].items():
            obj_dict[name] = params

        for area, obj_in_area in self.config_file["Areas"].items():
            for name, params in self.config_file["Areas"][area]["Objects"].items():
                obj_dict[name] = params
        return obj_dict

    def _get_mujoco_dict(self, obj_dict: dict):
        """Loads xml and parses with Parser class to mjcf and combines all information to a mujoco-object

        Parameters:
            obj_dict (dict): Contains information about world_container objects

        Returns:
            mujoco_dict (dict): Dictionary of world_container objects as mujoco-objects
        """
        mujoco_dict = {}
        for obj, params in obj_dict.items():
            obj_xml_path = os.path.join(self.xml_dir, obj + ".xml")
            mjcf = Parser.get_mjcf(xml_path=obj_xml_path)
            obj_type, attachable, colors, sizes = self._read_params(params)
            # ToDo: abfangen falls colors und sizes da ist..
            if not colors == None and not sizes == None:
                (
                    names,
                    mjcf_objs,
                    obj_types,
                    attachables,
                    colors_,
                    sizes_,
                ) = self._randomize_object()

            mujoco_obj = MujocoObject(
                name=obj,
                mjcf_obj=mjcf,
                obj_type=obj_type,
                attachable=attachable,
                colors=colors,
                sizes=sizes,
            )
            mujoco_dict[obj] = mujoco_obj
        return mujoco_dict

    @staticmethod
    def _read_params(params: list):
        """Helper function to read object specific parameters set in config file

        Parameters:
            params (list(dict)): List of world_container object specific parameters given as dictionary

        Returns:
            obj_type (str): Type of world_container-object; relates to mujoco-object parameter
            attachable (bool): True if object can be attached to a container-type object; relates to mujoco-object parameter
        """
        obj_type = None
        attachable = None
        colors = None
        sizes = None
        if not params == None:
            for dict_ in params:
                if "type" in dict_.keys():
                    obj_type = dict_["type"]
                if "attachable" in dict_.keys():
                    attachable = dict_["attachable"]
                if "colors" in dict_.keys():
                    colors = dict_["colors"]
                if "sizes" in dict_.keys():
                    sizes = dict_["sizes"]
        return obj_type, attachable, colors, sizes

    @staticmethod
    def _randomize_object(mjcf, colors: tuple[int, int], sizes: tuple[int, int]):
        # ToDo: ändere rgba und size
        names = list()
        mjcf_objs = list()
        obj_types = list()
        attachables = list()
        colors_ = list()
        sizes_ = list()

        # get random int in of range in colors
        colors_randint = (
            colors[0]
            if (colors[0] == colors[1])
            else np.random.randint(int(colors[0]), int(colors[1]))
        )

        # get random int in range of sizes
        sizes_randint = (
            sizes[0]
            if (sizes[0] == sizes[1])
            else np.random.randint(int(sizes[0]), int(sizes[1]))
        )

        # ToDo: logic für deepcopys der objekte und dann pars anpassen + "validierung" dass auch jede color 2 Mal vorkommt

        return names, mjcf_objs, obj_types, attachables, colors_, sizes_
