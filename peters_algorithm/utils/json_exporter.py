import json

from peters_algorithm.base.world_container.area import Area
from peters_algorithm.base.world_container.environment import Environment


class JSONExporter:

    @staticmethod
    def export(*, filename: str, environment: Environment, areas: list[Area]):
        """
        Parameters:
            filename (str):
            environment (Environment):
            areas (list):
        """
        all_objects = {'environment': {}, 'areas': {}}

        # environment loop
        for mujoco_object in environment._mujoco_objects.values():
            values = {}

            # values['mjcf_obj'] = mujoco_object.mjcf_obj
            values['type'] = mujoco_object.obj_type
            values['attachable'] = mujoco_object.attachable
            values['position'] = mujoco_object.position.tolist()
            # values['color'] = mujoco_object.color.tolist()
            # values['size'] = mujoco_object.size.tolist()
            # values['tag'] = mujoco_object.tag
            # values['id'] = mujoco_object.id

            all_objects['environment'][mujoco_object.name] = values

        # loop over all areas
        for area in areas:
            all_objects['areas'][area.name] = {}
            for mujoco_object in area._mujoco_objects.values():
                values = {}

                # values['mjcf_obj'] = mujoco_object.mjcf_obj
                values['type'] = mujoco_object.obj_type
                values['attachable'] = mujoco_object.attachable
                values['position'] = mujoco_object.position.tolist()
                # values['color'] = mujoco_object.color.tolist()
                # values['size'] = mujoco_object.size.tolist()
                # values['tag'] = mujoco_object.tag
                # values['id'] = mujoco_object.id

                all_objects['areas'][area.name][mujoco_object.name] = values

        with open("export/" + filename + ".json", 'w') as file:
            json.dump(all_objects, file, indent=4)
