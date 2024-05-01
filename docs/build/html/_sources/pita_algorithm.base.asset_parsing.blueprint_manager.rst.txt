Blueprint Manager Module
========================

Overview
--------

The Blueprint Manager module is a critical component of the PITA Algorithm, designed to manage and process blueprints for objects within the simulation environment. This module ensures that object blueprints are correctly parsed, stored, and accessible for the dynamic generation and placement of objects according to predefined or randomized parameters.

Key Features
------------

- **Blueprint Parsing and Storage**: Efficiently parses and stores object blueprints from YAML configuration files, allowing for quick retrieval and instantiation of objects during environment setup.
- **Dynamic Object Generation**: Facilitates the dynamic generation of objects based on blueprints, supporting extensive customization of object properties and behaviors for diverse simulation scenarios.
- **Integration with Object Placers**: Seamlessly integrates with fixed and random object placers, providing them with necessary blueprint information to accurately place objects within the simulation environment.
- **Modularity and Extensibility**: Designed with a focus on modularity, enabling easy extension to support new types of object blueprints and properties as research and simulation requirements evolve.

Usage
-----

The Blueprint Manager plays a pivotal role in the pre-simulation setup phase, where it processes and prepares object blueprints for use. By managing blueprints, it enables the system to instantiate objects with varied properties, enhancing the richness and diversity of the simulation environment.

1. **Blueprint Configuration**: Define object blueprints in a YAML file, including object properties and any special rules for instantiation.
2. **Blueprint Parsing**: On system initialization, the Blueprint Manager parses these configurations, preparing the blueprints for use.
3. **Object Instantiation**: During environment assembly, the Blueprint Manager supplies object placers with blueprints to create objects in the simulation according to the specified configurations.

This structured approach ensures that simulations can be rapidly prototyped and customized, supporting a wide range of research applications in artificial intelligence, reinforcement learning, and beyond.

.. automodule:: pita_algorithm.base.asset_parsing.blueprint_manager
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
