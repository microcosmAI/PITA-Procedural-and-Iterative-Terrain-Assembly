import json

from pita_algorithm.base.world_sites.area import Area
from pita_algorithm.base.world_sites.environment import Environment


class JSONExporter:
    """Exports all object information to a JSON file."""

    @staticmethod
    def export(
        export_path: str, config: dict, environment: Environment, areas: list[Area]
    ):
        """Export all object information from the given Environment and Area instances
        to a JSON file.

        Parameters:
            export_path (str): Path of the file to be exported
            config (dict): Config file containing user defined parameters
            environment (Environment): Environment class instance
            areas (list): List of Area class instances
        """
        # Dictionary to store all objects
        all_objects = {"environment": {}, "areas": {}}
        all_objects["environment"]["configuration"] = {}
        all_objects["environment"]["objects"] = {}

        values = {}
        # Extract all Environment configurations from the config apart from Objects and Borders
        for key, value in config["Environment"].items():
            if key != "Objects" and key != "Borders":
                values[key] = value
        all_objects["environment"]["configuration"] = values

        # Loop over Environment and its objects
        for mujoco_object in environment._mujoco_objects.values():
            values = {}

            values["name"] = mujoco_object.xml_id
            values[
                "type"
            ] = mujoco_object.obj_type  # TODO: Check if this is still needed
            values["class"] = mujoco_object.obj_class
            values["position"] = mujoco_object.position.tolist()
            values["color"] = mujoco_object.color.tolist()
            values["size"] = mujoco_object.size.tolist()
            values["tags"] = mujoco_object.tags

            all_objects["environment"]["objects"][mujoco_object.xml_id] = values

        # Loop over all Areas and their objects
        for area in areas:
            all_objects["areas"][area.name] = {}
            all_objects["areas"][area.name]["configuration"] = {}
            all_objects["areas"][area.name]["objects"] = {}

            values = {}
            # Extract all Area configurations from the config apart from Objects
            for key, value in config["Areas"][area.name.capitalize()].items():
                if key != "Objects":
                    values[key] = value
            all_objects["areas"][area.name]["configuration"] = values

            for mujoco_object in area._mujoco_objects.values():
                values = {}

                values["name"] = mujoco_object.xml_id
                values[
                    "type"
                ] = mujoco_object.obj_type  # TODO: Check if this is still needed
                values["class"] = mujoco_object.obj_class
                values["position"] = mujoco_object.position.tolist()
                values["color"] = mujoco_object.color.tolist()
                values["size"] = mujoco_object.size.tolist()
                values["tags"] = mujoco_object.tags

                all_objects["areas"][area.name]["objects"][
                    mujoco_object.xml_id
                ] = values

        # Export to JSON file
        with open(export_path + ".json", "w") as file:
            json.dump(all_objects, file, indent=4)
