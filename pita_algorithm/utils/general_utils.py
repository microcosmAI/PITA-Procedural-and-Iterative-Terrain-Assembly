class Utils:
    """Collection of utility functions."""

    @staticmethod
    def get_randomization_parameters(config_dict: dict, keys: list) -> tuple:
        """Reads the randomization parameters in config_dict for the given keys.

        Parameters:
            config_dict (dict): Contains information about world settings
            keys (list): List of keys to read from the config_dict

        Returns:
            tuple: Tuple containing the values for the given keys in the order they were passed
        """
        # Initialize default values
        default_values = [None] * len(keys)

        # Loop over keys and update default values
        for i, key in enumerate(keys):
            if key in config_dict:
                default_values[i] = config_dict[key]

        return tuple(default_values)

    @staticmethod
    def offset_coordinates_to_boundaries(
        position: tuple[float, float, float],
        boundary: tuple[tuple[float, float], tuple[float, float]],
        reference_boundaries: tuple[tuple[float, float], tuple[float, float]],
    ) -> tuple[float, float, float]:
        """
        Converts the coordinates of a MujocoObject to match the boundaries of the Area.

        Parameters:
            position (tuple[float, float, float]): The coordinates of the MujocoObject.
            boundary (tuple[tuple[float, float], tuple[float, float]]): The boundaries of the Area.
            reference_boundaries (tuple[tuple[float, float], tuple[float, float]]): The boundaries of the reference
                                                                                    Area -> Environment Size.

        Returns:
            tuple[float, float, float]: The converted coordinates.
        """
        small_x1, small_y1 = boundary[0]
        small_x2, small_y2 = boundary[1]
        big_x1, big_y1 = reference_boundaries[0]
        big_x2, big_y2 = reference_boundaries[1]

        # Calculate dimensions of both rectangles
        small_width = small_x2 - small_x1
        small_height = small_y2 - small_y1
        big_width = big_x2 - big_x1
        big_height = big_y2 - big_y1

        # Adjust the input coordinates based on the lower left coordinate of the big rectangle
        adjusted_x = position[0] - big_x1
        adjusted_y = position[1] - big_y1

        # Scale these adjusted coordinates according to the size ratio of the small and big rectangles
        scaled_x = (adjusted_x * small_width) / big_width
        scaled_y = (adjusted_y * small_height) / big_height

        # Add the lower left corner coordinates of the small rectangle to offset the coordinates properly
        final_x = small_x1 + scaled_x
        final_y = small_y1 + scaled_y

        return final_x, final_y, position[2]
