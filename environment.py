from dm_control import mjcf
import Area


class Environment:
    "Class that represents the entire environment"

    def __init__(
        self,
        size: tuple[int, int],
        border: tuple[tuple[int, int, str], ...],
        areas: tuple[Area, ...],
    ):
        """Initializes the environment class

        Parameters:
            size (tuple): Tuple defining the size of the entire environment
            border (tuple): Defines the borders surrounding the environment and their respective types
            areas (tuple): Areas dividing the environment into different segments with different properties
        """
        self.size = size
        self.border = border
        self.area = areas
        self.mjcf_model = mjcf.RootElement()
