MuJoCo Object Module
====================

Overview
--------

Central to the PITA Algorithm's simulation capabilities, the `mujoco_object` module facilitates the representation and manipulation of objects within the MuJoCo physics engine. It defines the `MujocoObject` class, which serves as a wrapper for MuJoCo's physical entities, providing a unified interface for creating, configuring, and interacting with simulation objects.

Key Features
------------

- **Unified Object Interface**: Provides a standardized approach to define and interact with objects across various simulations, streamlining the object creation process.
- **Detailed Property Configuration**: Allows for the detailed specification of physical properties, such as mass, size, texture, and collision parameters, ensuring objects behave as expected within the simulation environment.
- **Dynamic Interaction Support**: Supports dynamic interactions within the simulation, including object manipulation and response to physical forces, enhancing the realism and applicability of simulation scenarios.
- **Extensibility for Custom Properties**: Designed with extensibility in mind, enabling the addition of custom properties and behaviors to meet specific research requirements.

Usage
-----

The `MujocoObject` class is utilized throughout the simulation lifecycle, from the initial setup phase, where objects are defined and added to the simulation, through to runtime, where objects may be manipulated or queried for state information. Here's an outline of its typical use:

1. **Object Definition**: Define objects using the `MujocoObject` class, specifying necessary properties and attributes according to simulation requirements.
2. **Simulation Integration**: Add these objects to the simulation environment, where they are instantiated within the MuJoCo physics engine.
3. **Runtime Manipulation**: Interact with objects during simulation execution, applying forces, updating properties, or querying state information as needed.

By abstracting away the complexities of direct MuJoCo engine manipulation, the `mujoco_object` module significantly simplifies the process of incorporating detailed physical simulations into research projects.


.. automodule:: pita_algorithm.base.asset_parsing.mujoco_object
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
