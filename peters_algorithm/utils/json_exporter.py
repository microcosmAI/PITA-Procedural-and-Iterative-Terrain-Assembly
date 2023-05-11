import json

from peters_algorithm.base.world_container.area import Area
from peters_algorithm.base.world_container.environment import Environment


class JSONExporter:
    """Exports all object information to a json file"""

    @staticmethod
    def export(*, filename: str, environment: Environment, areas: list[Area]):
        """Export all object information from the given Environment and Area instances to a json file

        Parameters:
            filename (str): Name of the file to be exported
            environment (Environment): Environment class instance
            areas (list): List of Area class instances
        """
        # Dictionary to store all objects
        all_objects = {"environment": {}, "areas": {}}

        # Loop over Environment and its objects
        for mujoco_object in environment._mujoco_objects.values():
            values = {}

            # values['mjcf_obj'] = mujoco_object.mjcf_obj
            values["type"] = mujoco_object.obj_type
            values["attachable"] = mujoco_object.attachable
            values["position"] = mujoco_object.position.tolist()
            # values['color'] = mujoco_object.color.tolist()
            # values['size'] = mujoco_object.size.tolist()
            # values['tag'] = mujoco_object.tag
            # values['id'] = mujoco_object.id

            all_objects["environment"][mujoco_object.name] = values

        # Loop over all Areas and their objects
        for area in areas:
            all_objects["areas"][area.name] = {}
            for mujoco_object in area._mujoco_objects.values():
                values = {}

                # values['mjcf_obj'] = mujoco_object.mjcf_obj
                values["type"] = mujoco_object.obj_type
                values["attachable"] = mujoco_object.attachable
                values["position"] = mujoco_object.position.tolist()
                # values['color'] = mujoco_object.color.tolist()
                # values['size'] = mujoco_object.size.tolist()
                # values['tag'] = mujoco_object.tag
                # values['id'] = mujoco_object.id

                all_objects["areas"][area.name][mujoco_object.name] = values

        # Export to json
        with open("export/" + filename + ".json", "w") as file:
            json.dump(all_objects, file, indent=4)
