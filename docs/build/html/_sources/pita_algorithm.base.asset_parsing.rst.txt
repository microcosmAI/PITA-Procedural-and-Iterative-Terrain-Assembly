Asset Parsing Package
=====================

Overview
--------

The `asset_parsing` package within the PITA Algorithm framework serves as a comprehensive suite for handling the parsing, loading, and management of simulation assets. This includes interpreting object blueprints, initializing objects with the MuJoCo physics engine, and managing the lifecycle of these objects within simulation environments.

Key Features
------------

- **Blueprint Management**: Facilitates the parsing and storage of object blueprints from configuration files, enabling dynamic instantiation of objects with varied properties.
- **MuJoCo Integration**: Seamlessly interfaces with the MuJoCo physics engine, translating parsed asset specifications into physical entities within the simulation.
- **Flexible Asset Configuration**: Supports a broad range of asset definitions and configurations, from simple geometric shapes to complex, behaviorally-rich entities.
- **Enhanced Simulation Realism**: By allowing detailed specification and manipulation of assets, the package contributes significantly to the realism and depth of simulation scenarios, enabling more nuanced and varied research experiments.

Components
----------

The `asset_parsing` package comprises several modules, each dedicated to specific aspects of asset handling within the PITA Algorithm framework:

- **`blueprint_manager`**: Manages the retrieval and storage of object blueprints, ensuring that objects can be dynamically generated based on predefined templates.
- **`mujoco_loader`**: Responsible for loading assets into the MuJoCo simulation environment, applying physical properties and behaviors as defined in their blueprints.
- **`mujoco_object`**: Defines the `MujocoObject` class, a wrapper for simulation objects that facilitates interaction with the MuJoCo physics engine.
- **`parser`**: Parses simulation configurations and object definitions from external files, translating them into actionable specifications for simulation setup.

Usage
-----

The `asset_parsing` package is typically utilized during the simulation setup phase, where it processes configuration files and initializes the simulation environment:

1. **Configuration Processing**: Object and environment configurations are parsed from external files, detailing the specifications for each simulation asset.
2. **Asset Initialization**: These specifications are used to instantiate and configure objects within the MuJoCo simulation, leveraging the package's integration with the physics engine.
3. **Simulation Execution**: With assets loaded and configured, the simulation can proceed, benefiting from the detailed and dynamic environments made possible by the `asset_parsing` package.

This package underpins the PITA Algorithm's ability to generate richly detailed and highly customizable simulation environments, supporting a wide range of research applications in artificial intelligence, machine learning, and robotics.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   blueprint_manager
   mujoco_loader
   mujoco_object
   parser


.. automodule:: pita_algorithm.base.asset_parsing
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

Submodules
----------

.. toctree::
   :maxdepth: 5

   pita_algorithm.base.asset_parsing.blueprint_manager
   pita_algorithm.base.asset_parsing.mujoco_loader
   pita_algorithm.base.asset_parsing.mujoco_object
   pita_algorithm.base.asset_parsing.parser
