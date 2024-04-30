Validator Module
===============

Overview
--------

The `Validator` class plays a pivotal role in the PITA Algorithm framework, ensuring that new object placements comply with a predefined set of rules. It validates objects against these rules and maintains a 2D representation of the environment, facilitating both compliance checks and visualization of the simulation space.

Key Features
------------

- **Rule-Based Validation**: Leverages a list of rules to validate new object placements, ensuring that all objects comply with the specified constraints before being added to the simulation.

- **2D World Representation**: Maintains a 2D map of the simulation environment, providing a visual representation of object placements and aiding in the detection of rule violations.

- **Dynamic Rule Application**: Allows for the dynamic addition of rules, offering flexibility in defining the constraints that objects must satisfy within the simulation.

Usage
-----

The `Validator` class within your simulation setup:

1. **Initialization**: The `Validator` class is Instantiated with a list of `Rule` objects that new placements must satisfy.

2. **Object Validation**: The `validate` method checks whether a new object satisfies all the specified rules based on its intended placement and the current state of the simulation environment.

3. **Visualization**: The `plot` method can be used to visualize the current 2D representation of the environment and the placements of objects within it.


.. automodule:: pita_algorithm.base.asset_placement.validator
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
