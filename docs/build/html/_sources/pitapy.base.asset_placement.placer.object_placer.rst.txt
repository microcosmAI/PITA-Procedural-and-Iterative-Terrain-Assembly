ObjectPlacer Class
==================

Overview
--------

The `ObjectPlacer` class orchestrates the placement of objects across the simulation environment, leveraging predefined configurations to automate the process. It encapsulates the logic for adding borders, fixed, and random objects to both global environments and specific areas, streamlining the setup of complex simulation scenarios.

Functionalities
---------------

- **Border Placement**: Automatically places border objects around the environment, enhancing the simulation's visual boundaries and structural definition.

- **Fixed and Random Object Placement**: Depending on the configuration, places objects at fixed coordinates or distributes them randomly, offering versatility in simulation design.

- **Configurable Object Properties**: Supports the customization of object properties such as size, color, and rotation, directly influencing the simulation's dynamics and aesthetics.

Usage
-----

Upon initialization, `ObjectPlacer` requires a configuration dictionary and a set of object blueprints:

1. **Configuration**: Defines the placement and properties of objects to be added to the simulation, including specifics for borders, fixed objects, and random objects.

2. **Blueprints**: Provides templates for each type of object that might be placed, ensuring accurate reproduction of object properties.

The placement process involves iterating over the environment and areas, placing objects according to their designated settings in config.yml


.. automodule:: pitapy.base.asset_placement.placer.object_placer
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
