MinDistanceRule Module
=====================

Overview
--------

The `MinDistanceRule` class enforces a spatial constraint ensuring that newly placed objects respect a specified minimum distance from other objects in the simulation environment. This rule is crucial for preventing undesired overlaps or ensuring safety margins between objects, enhancing the realism and accuracy of simulations.

Key Features
------------

- **Minimum Distance Enforcement**: Validates that each new object is placed at least a specified distance away from existing objects, according to their geometric representations.

- **Selective Type Validation**: Allows specifying object types to which the minimum distance constraint should be applied, offering flexibility in rule enforcement across different object classes.

- **Broad Applicability**: Works with any object represented by Shapely's geometric objects, providing a versatile solution for distance-based validation in a variety of simulation contexts.

Usage
-----

`MinDistanceRule` is used within the simulation setup:

1. **Initialization**: Instantiate the rule with the desired minimum distance and optionally, a list of object types to which the rule should be specifically applied.
   
2. **Rule Application**: Integrates the rule into the object placement process to validate the placement of new objects, ensuring they adhere to the specified minimum distance constraint provided in config.yml or default


.. automodule:: pita_algorithm.base.asset_placement.rules.min_distance_rule
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
