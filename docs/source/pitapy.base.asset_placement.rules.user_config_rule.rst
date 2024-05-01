User Config Rules Module
===============

Overview
--------

The `UserRules` class is designed to parse and extract simulation rules from a configuration dictionary, enabling the dynamic application of both default and user-defined rules across simulation environments. This class facilitates the customization of simulation behaviors and constraints based on specific user requirements, enhancing the flexibility and adaptability of simulations.

Key Features
------------

- **Configuration-Based Rule Extraction**: Parses the provided configuration dictionary to identify and extract specified simulation rules.

- **Default and Custom Rule Support**: Applies a set of default rules when custom rules are not specified, ensuring baseline constraints are always in place.

- **Flexible Rule Specification**: Accommodates a wide range of rule types and parameters, allowing for detailed customization of simulation constraints.

Usage
-----

The `UserRules` class within the simulation setup:

1. **Initialization**: Instantiates the `UserRules` class with the simulation's configuration dictionary containing rule definitions.

2. **Rule Extraction**: It Employs the `extract_rules` and `get_rules` methods to retrieve rule sets for specific sites or the entire environment, based on the configuration yml.


.. automodule:: pitapy.base.asset_placement.rules.user_config_rule
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
