Placer Classes in PITA Algorithm
================================

The placer classes within the PITA Algorithm framework facilitate the placement of objects within the simulation environment, offering a range of strategies from fixed and random placements to specialized border and object placements. These classes share a common goal of enhancing the realism and variability of simulation scenarios, each serving a unique role in the object placement process.

AbstractPlacer
--------------

The base class for all placement strategies, defining a common interface and essential functionalities for object placement. It is not instantiated directly but extended by specific placer classes to implement concrete placement logic.

FixedPlacer
-----------

Derives from `AbstractPlacer`, providing functionality to place objects at predetermined coordinates within the environment. It ensures precise control over object arrangements, ideal for simulations requiring specific spatial relationships between objects.

RandomPlacer
------------

Also extending `AbstractPlacer`, this class introduces randomness to object placement, allowing objects to be distributed across the environment according to specified distribution patterns. It supports a range of distribution strategies, enabling diverse simulation setups.

BorderPlacer
------------

A specialized placer focused on the addition of border objects around the perimeter of the simulation environment. It automates the process of enclosing the simulation space, enhancing environmental structure and boundary definition.

ObjectPlacer
------------

A high-level class that orchestrates the placement of all types of objects within the simulation, leveraging the functionality of the other placer classes. It handles the overall object placement process, from borders to fixed and random objects, according to the simulation's configuration.


.. automodule:: pita_algorithm.base.asset_placement.placer
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

Submodules
----------

.. toctree::
   :maxdepth: 5

   pita_algorithm.base.asset_placement.placer.abstract_placer
   pita_algorithm.base.asset_placement.placer.border_placer
   pita_algorithm.base.asset_placement.placer.fixed_placer
   pita_algorithm.base.asset_placement.placer.object_placer
   pita_algorithm.base.asset_placement.placer.random_placer
