FixedPlacer Class
=================

Overview
--------

The `FixedPlacer` class, deriving from the `AbstractPlacer`, specializes in the deterministic placement of objects within the simulation environment. It allows for the precise positioning of objects based on predefined coordinates, making it ideal for simulations requiring strict control over object locations.

Functionalities
---------------

- **Fixed Object Placement**: Facilitates the exact placement of objects at specified coordinates within the environment, ensuring a consistent setup across simulation runs.

- **Property Customization**: Supports customization of object properties, such as color, size, and z-axis rotation, at the time of placement, enabling detailed control over the appearance and orientation of objects.

- **Validation and Collision Avoidance**: Utilizes validators to ensure that proposed placements do not violate any environmental constraints or result in unintended overlaps with existing objects.

Usage
-----

The `FixedPlacer` class is used to add objects to a simulation environment or area with fixed coordinates:

1. **Initialization**: Instantiate the `FixedPlacer` without any specific parameters.
   
2. **Adding Objects**: Use the `add` method to place objects into the site, providing the necessary details including the object blueprint, validators, and placement properties such as coordinates and rotations.

3. **Object Removal**: Implement the `remove` method to delete objects from the site, maintaining the environment's integrity and flexibility.


.. automodule:: pitapy.base.asset_placement.placer.fixed_placer
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
