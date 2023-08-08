class Utils:
    @staticmethod
    def _get_randomization_parameters(config_dict: dict, keys: list) -> tuple:
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
