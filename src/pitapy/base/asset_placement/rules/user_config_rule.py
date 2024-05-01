import logging
from typing import Union


class UserRules:
    """Class to extract rules from a configuration dictionary."""

    def __init__(self, config: dict):
        """Constructor of the UserRules class.

        Parameters:
            config (dict): The configuration dictionary
        """
        self.config = config
        self.default_rules = {
            "MinAllDistance": {"distance": 1.0},
            "Boundary": None,
            "Height": {"ground_level": 0.0},
        }

    def extract_rules(self, data: dict, site_name: str) -> Union[dict, None]:
        """Extracts the rules from data.

        Parameters:
            data (dict): The data from which to extract the rules
            site_name (str): The name of the site

        Returns:
            (dict, None): The extracted or default rules, None if data is not a dictionary
        """
        logger = logging.getLogger()
        if isinstance(data, dict):
            # If rules are specified in the configuration, extract them
            try:
                rule_dict = {}
                # Find rules specified via the Rules key in the config
                for rule in data.get("Rules"):
                    for rule_name, parameters in rule.items():
                        result_dict = {}
                        # If the rule has parameters, add them to the result dictionary
                        if isinstance(parameters, list):
                            for parameter in parameters:
                                result_dict.update(parameter)
                        # If the rule has no parameters, set the corresponding value to None
                        else:
                            result_dict = None
                        rule_dict[rule_name] = result_dict
                return rule_dict

            # If no rules are specified, return the default rules
            except TypeError:
                logger.info(
                    f"No rules specified for '{site_name}'. Using default rules: '{self.default_rules}'."
                )
                return self.default_rules
        return None

    def get_rules(self) -> Union[dict, None]:
        """Extracts all the rules from the configuration dictionary.

        Returns:
            (dict, None): The extracted rules
        """
        if not self.config:
            print("Failed to load configuration.")
            return None

        rules_dict = {}

        # Extract rules for the Environment
        environment_rules = self.extract_rules(
            self.config.get("Environment", {}), "Environment"
        )
        if environment_rules:
            rules_dict["Environment"] = environment_rules

        # Extract rules for each Area
        for area_name, area_data in self.config.get("Areas", {}).items():
            area_rules = self.extract_rules(area_data, area_name)
            if area_rules:
                rules_dict.setdefault(area_name, area_rules)

        return rules_dict
