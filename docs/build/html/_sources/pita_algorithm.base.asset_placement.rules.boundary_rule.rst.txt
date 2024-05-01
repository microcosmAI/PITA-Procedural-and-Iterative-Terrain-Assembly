Boundary Rule Class
==================

Overview
--------

The `BoundaryRule` class extends the `Rule` abstract class to provide a specific implementation that checks whether objects are placed within predefined spatial boundaries. Utilizing geometric constraints, this rule ensures that object placements do not exceed the limits of the simulation environment or designated areas, maintaining the integrity and realism of simulations.

Key Features
------------

- **Geometric Boundary Checking**: Uses Shapely's geometric capabilities to define and check boundaries, ensuring object placements fall within the specified area.
  
- **Flexible Boundary Definitions**: Allows for the dynamic definition of boundaries using tuples, making it adaptable to various simulation environments and scenarios.

- **Integration with Object Placement**: Seamlessly integrates with the object placement process, offering a straightforward method to enforce spatial constraints on placed objects.


.. automodule:: pita_algorithm.base.asset_placement.rules.boundary_rule
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
