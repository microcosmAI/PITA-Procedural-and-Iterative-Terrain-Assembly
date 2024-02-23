from typing import Union
from pita_algorithm.base.asset_placement.rules.height_rule import HeightRule
from pita_algorithm.base.asset_placement.rules.boundary_rule import BoundaryRule
from pita_algorithm.base.asset_placement.rules.min_distance_mujoco_physics_rule import (
    MinDistanceMujocoPhysicsRule,
)


class RuleAssembler:
    """Represents a mapping between rule names and rule objects,
    and assembles site rule pairings based on user rules.
    """

    def __init__(self, userrules):
        """Constructor of the RuleAssembler class.

        Parameters:
            userrules (dict): Dictionary containing user rules
        """
        self.user_rules = userrules

    def _get_rule_object(
        self, rule_name: str, userrule: dict, environment_size: list
    ) -> Union[HeightRule, BoundaryRule, MinDistanceMujocoPhysicsRule]:
        """Returns the appropriate rule object based on the rule name.

        Parameters:
            rule_name (str): Name of the rule
            userrule (dict): Dictionary containing rule details
            environment_size (list): Size of the environment

        Returns:
            Rule: Rule object

        Raises:
            ValueError: If the rule name is unknown
        """
        # More conditions as fitting can be added here as more rules are added
        if rule_name == "MinAllDistance":
            return MinDistanceMujocoPhysicsRule(distance=userrule.get("distance"))
        elif rule_name == "Height":
            return HeightRule(ground_level=userrule.get("ground_level"))
        elif rule_name == "Boundary":
            return BoundaryRule(boundary=(environment_size[0], environment_size[1]))
        else:
            raise ValueError(f"Unknown rule name: {rule_name}")

    def assemble_site_rules_pairs(self, environment_size: list) -> dict:
        """Assembles Site and Rule pairs based on user rules.

        Parameters:
            environment_size (list): Size of the environment

        Returns:
            site_rule_pairs (dict): Dictionary containing site and rule pairs
        """
        site_rule_pairs = {}
        for site, site_rules in self.user_rules.items():
            site_rule_pairs[site] = []
            for rule_name, rule_parameters in site_rules.items():
                site_rule_pairs[site].append(
                    self._get_rule_object(rule_name, rule_parameters, environment_size)
                )

        return site_rule_pairs
