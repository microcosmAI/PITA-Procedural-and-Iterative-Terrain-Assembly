from dm_control import mjcf


class Environment:
    """Class that represents the entire environment"""

    def __init__(self, size: tuple[float, float, float]):
        """
        Initializes the environment class

        Parameters:
            size (tuple): Tuple defining the size of the entire environment
        """
        self.size = size
        self.mjcf_model = mjcf.RootElement()
        self.mjcf_model.worldbody.add(
            "geom", name="base_plane", type="plane", size=size
        )
