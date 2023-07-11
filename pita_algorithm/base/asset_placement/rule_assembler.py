class RuleAssembler:
    """
    Represents a mapping between rule names and rule objects,
    and assembles rule objects based on user rules, with other important usable methods
    """
    
    def __init__(self, userrules):
        """
        Initializes an instance of RuleAssembler.
        """
        self.user_validators = self._assemble_rules(userrules)

        self.user_validators = self._assemble_rules(userrules)
        
    def _assemble_rules(self, userrules):
        """
        Private method to assemble rule objects from user rules.

        Args:
            userrules (dict): Dictionary containing user rules.

        Returns:
            dict: Dictionary containing assembled rule objects.
        """
        validators = {}
        for category, category_rules in userrules.items():
            validators[category] = {}
            if "rules" in category_rules:
                # For nested rule entries
                for rule_dict in category_rules["rules"]:
                    for rulename, rule_details in rule_dict.items():
                        rule_obj = self._get_rule_object(rulename, rule_details)
                        validators[category][rulename] = rule_obj
            else:
                # For non-nested rule entries
                for subcategory, subcategory_rules in category_rules.items():
                    validators[category][subcategory] = {}
                    for rule_dict in subcategory_rules["rules"]:
                        for rulename, rule_details in rule_dict.items():
                            rule_obj = self._get_rule_object(rulename, rule_details)
                            validators[category][subcategory][rulename] = rule_obj
        return validators
    
    def _get_rule_object(self, rulename, userrule):
        """
        Returns the appropriate rule object based on the rule name.

        Args:
            rulename (str): Name of the rule.
            userrule (dict): Dictionary containing rule details.

        Returns:
            dict: Rule object.

        Raises:
            ValueError: If the rule name is unknown.
        """
        # More conditions as fitting can be added here as we develop further
        if rulename == "MinObjectDistance":
            return {
                'type': 'MinObjectDistance',
                'target_object': userrule[1].get("object"),
                'distance': userrule[0].get("distance")
            }
        elif rulename == "MinAllDistance":
            return {
                'type': 'MinAllDistance',
                'distance': userrule[0].get("distance")
            }
        elif rulename == "Vanish":
            return {
                'type': 'Vanish',
                'van': userrule.get("van")
            }
        else:
            raise ValueError(f"Unknown rule name: {rulename}")

    def get_rule_attribute(self, category, rule_name, attribute):
        """
        Method to get a specific attribute value of a rule object in a given category by rule name.

        Args:
            category (str): Rule category.
            rule_name (str): Rule name.
            attribute (str): Rule attribute.

        Returns:
            any: Value of the rule attribute or None if not found.
        """
        try:
            return self.user_validators[category][rule_name][attribute]
        except KeyError:
            return None

    
    def filter_rules(self, category=None, subcategory=None, rule_name=None, attribute=None):
        """
        Filters and returns rules based on category, subcategory, rule name, and attribute.
        
        Args:
            category (str, optional): The category to filter by (e.g. "Environment", "Area1").
            subcategory (str, optional): The subcategory to filter by. (e.g "Tree", "Stone")
            rule_name (str, optional): The rule name to filter by.
            attribute (str, optional): The attribute within the rule to filter by.

        Returns:
            dict or any: A dictionary containing the filtered rules or specific attribute value.
        """
        result = self.user_validators
        
        if category is not None:
            result = result.get(category, {})
            
        if subcategory is not None:
            result = result.get(subcategory, {})
            
        if rule_name is not None:
            result = result.get(rule_name, {})
            
        if attribute is not None:
            if isinstance(result, dict):
                return result.get(attribute)
            else:
                return None
            
        return result
    
    def add_rule(self, category, rule_obj, subcategory=None):
        """
        Adds a new rule to an existing category, subcategory or a completely new category or subcategory.

        Args:
            category (str): The category to which the rule is to be added.
            rule_obj (dict): The rule to be added.
            subcategory (str, optional): The subcategory to which the rule is to be added. Defaults to None.
        """
        if subcategory:
            if category not in self.user_validators:
                self.user_validators[category] = {}
            self.user_validators[category][subcategory] = rule_obj
        else:
            self.user_validators[category] = rule_obj

    def remove_rule(self, category, subcategory=None, rule_name=None):
        """
        Removes an existing rule.

        Args:
            category (str): The category from which the rule is to be removed.
            subcategory (str, optional): The subcategory from which the rule is to be removed. Defaults to None.
            rule_name (str, optional): The specific rule to be removed. Defaults to None.
        """
        if subcategory:
            if rule_name:
                del self.user_validators[category][subcategory][rule_name]
            else:
                del self.user_validators[category][subcategory]
        else:
            del self.user_validators[category]

    def update_rule(self, category, rule_obj, subcategory=None):
        """
        Updates an existing rule.

        Args:
            category (str): The category in which the rule is to be updated.
            rule_obj (dict): The updated rule.
            subcategory (str, optional): The subcategory in which the rule is to be updated. Defaults to None.
        """
        self.add_rule(category, rule_obj, subcategory)

    def validate_rules(self):
        """
        Checks if all the rules in the rule set are valid according to some criteria.
        """
        # Example validation: ensure each rule has a 'type' key
        for category, rules in self.user_validators.items():
            for subcategory, sub_rules in rules.items():
                for rule_name, rule in sub_rules.items():
                    if 'type' not in rule:
                        print(f"Rule {rule_name} in category {category}/{subcategory} is missing 'type' key.")

    def apply_rules(self, object):
        """
        Applies the rules to an object.

        Args:
            object (any): The object to which the rules are to be applied.
        """
        # The loic of this will be dependent on what we need to do in later.
        pass

    def export_rules(self, filename):
        """
        Exports the current rule set to a file.

        Args:
            filename (str): The file to which the rule set is to be exported.
        """
        import json
        with open(filename, 'w') as f:
            json.dump(self.user_validators, f)

    def search_rules(self, search_term):
        """
        Searches through the rules based on a search term.

        Args:
            search_term (str): The term to search for in the rules.

        Returns:
            dict: A dictionary containing all the rules that match the search term.
        """
        results = {}
        for category, rules in self.user_validators.items():
            for subcategory, sub_rules in rules.items():
                for rule_name, rule in sub_rules.items():
                    if search_term in rule_name:
                        if category not in results:
                            results[category] = {}
                        if subcategory not in results[category]:
                            results[category][subcategory] = {}
                        results[category][subcategory][rule_name] = rule
        return results
