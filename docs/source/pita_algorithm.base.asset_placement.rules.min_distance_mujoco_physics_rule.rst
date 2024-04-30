MinDistanceMujocoPhysicsRule Module
==================================

Overview
--------

The `MinDistanceMujocoPhysicsRule` class is designed to enforce a minimum distance constraint between objects in a simulation environment powered by the MuJoCo physics engine. This rule is particularly useful in simulations where physical interactions and collisions between objects must be managed to ensure realistic behavior and outcomes.

Key Features
------------

- **Physics-based Validation**: Utilizes the MuJoCo physics engine to accurately determine the physical interactions between objects, providing a robust method for enforcing spatial constraints.

- **Minimum Distance Enforcement**: Ensures that a new object respects a specified minimum distance from all existing objects, preventing undesired overlaps and ensuring realistic object placements.

- **Dynamic Attachment and Detachment**: Temporarily attaches the new object to the simulation model for collision checking, then detaches it, allowing for efficient validation without permanent alterations to the simulation state.

Usage
-----

The `MinDistanceMujocoPhysicsRule` is used in the simulation setup:

1. **Initialization**: The rule is instantiated with the desired minimum distance between objects, default or provided in config.yml.
   
2. **Object Placement Validation**: During the object placement process, the rule is applied to validate the placement of new objects, ensuring they adhere to the specified minimum distance from existing objects.


.. automodule:: pita_algorithm.base.asset_placement.rules.min_distance_mujoco_physics_rule
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
