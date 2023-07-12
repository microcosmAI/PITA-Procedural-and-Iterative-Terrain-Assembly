class UserRules:
    """Class to extract rules from a configuration dictionary."""

    def __init__(self, config):
        """
        Initializes the UserRules class.

        Args:
            config (dict): The configuration dictionary.
        """
        self.config = config

    def extract_rules(self, data):
        """
        Extracts the rules from data.

        Parameters:
            data (dict or list): The data from which to extract the rules.

        Returns:
            list or None: The extracted rules if found, None otherwise.
        """
        if isinstance(data, dict):
            return data.get("rules")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "rules" in item:
                    return item.get("rules")
        return None

    def extract_object_rules(self, objects, rules_dict, parent_keys=None):
        """
        Extracts object-specific rules from the given objects.

        Parameters:
            objects (dict): The objects dictionary.
            rules_dict (dict): The dictionary to store rules.
            parent_keys (list): The list of keys indicating the current hierarchy.
        """
        parent_keys = parent_keys or []

        for obj_name, obj_data in objects.items():
            obj_rules = self.extract_rules(obj_data)
            current_keys = parent_keys + [obj_name]

            if obj_rules:
                temp = rules_dict
                for key in current_keys:
                    temp = temp.setdefault(key, {})
                temp["rules"] = obj_rules

            # Check for nested objects
            if isinstance(obj_data, dict) and "Objects" in obj_data:
                nested_objects = obj_data["Objects"]
                self.extract_object_rules(nested_objects, rules_dict, current_keys)

    def get_rules(self):
        """
        Extracts all the rules from the configuration dictionary.

        Returns:
            dict: The extracted rules.
        """
        if not self.config:
            print("Failed to load configuration.")
            return None

        rules_dict = {}

        # Extract rules for the Environment
        environment_rules = self.extract_rules(self.config.get("Environment", {}))
        if environment_rules:
            rules_dict["Environment"] = {"rules": environment_rules}

        # Extract rules for the objects in the Environment
        self.extract_object_rules(
            self.config.get("Environment", {}).get("Objects", {}),
            rules_dict,
            ["Environment"],
        )

        # Extract rules for each Area and the objects within them
        for area_name, area_data in self.config.get("Areas", {}).items():
            area_rules = self.extract_rules(area_data)
            if area_rules:
                rules_dict.setdefault(area_name, {})["rules"] = area_rules

            self.extract_object_rules(
                area_data.get("Objects", {}), rules_dict, [area_name]
            )

        return rules_dict
