from dm_control import mjcf
import Site


class Environment(Site):
    """Class that represents the entire environment"""

    def __init__(self, size: tuple[float, float, float]):
        """
        Initializes the environment class

        Parameters:
            size (tuple): Tuple defining the size of the entire environment
        """
        super(Environment, self).__init__()

        self.size = size
        self.mjcf_model = mjcf.RootElement()
        self.mjcf_model.worldbody.add(
            "geom", name="base_plane", type="plane", size=size
        )

    def add(self, mujoco_object: mjcf.RootElement):
        """
        Adds a mujoco object

        Parameters:
            mujoco_object (mjcf): Tuple defining the size of the entire environment
        """
        self.mjcf_model.attach(mujoco_object)

    def remove(self, mujoco_object: mjcf.RootElement):
        """
        Removes a given mujoco object

        Parameters:
            mujoco_object (mjcf): Tuple defining the size of the entire environment
        """
        mujoco_object.detach()
