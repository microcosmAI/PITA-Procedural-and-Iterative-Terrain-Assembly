class MujocoLoader:
    """ class to load mujoco objects "

    ToDo: a lot; in progress
    """

    def __init__(self, config_file: dict):
        self.config_file = config_file

    def get_mujoco_objects(self):
        dict_ = self._create_dict_of_objects()
        return dict_

    def _get_info_of_obj(self):
        pass

    def _create_dict_of_objects(self):
        pass
