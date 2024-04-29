MuJoCo Loader Module
====================

Overview
--------

The MuJoCo Loader module within the PITA Algorithm infrastructure is tasked with loading and initializing MuJoCo-specific objects for use in simulations. It acts as the bridge between the abstract representations of objects within the PITA framework and their concrete implementations within the MuJoCo physics engine, ensuring that objects are not only correctly instantiated but also possess the necessary physical properties for accurate simulation.

Key Features
------------

- **Direct Integration with MuJoCo**: Offers seamless integration with the MuJoCo physics engine, translating abstract object blueprints into fully functional MuJoCo objects.
- **Physical Property Assignment**: Ensures that all objects loaded into the simulation are endowed with the correct physical properties, such as mass, friction, and geometry, as defined in their blueprints.
- **Dynamic Object Instantiation**: Supports the dynamic instantiation of objects, allowing simulations to introduce or remove objects at runtime, facilitating studies on dynamic environments.
- **Extensible Object Support**: Designed to be easily extendable, the loader can accommodate new types of objects and properties, supporting ongoing research and development needs.

Usage
-----

The MuJoCo Loader is integral to the simulation initialization process, preparing and loading objects into the environment based on their specified blueprints. Here's a high-level overview of its role in the simulation setup:

1. **Initialization**: At the start of a simulation, the MuJoCo Loader reads object blueprints and begins the process of instantiation within the MuJoCo environment.
2. **Property Mapping**: It maps specified properties from the blueprints to their corresponding MuJoCo attributes, ensuring that objects behave as expected within the simulation.
3. **Runtime Flexibility**: Throughout the simulation, the loader can be called upon to add or remove objects, allowing for dynamic changes within the simulation environment.

The MuJoCo Loader module ensures that the PITA Algorithm's simulations are both versatile and physically accurate, leveraging the full capabilities of the MuJoCo physics engine.


.. automodule:: pita_algorithm.base.asset_parsing.mujoco_loader
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
