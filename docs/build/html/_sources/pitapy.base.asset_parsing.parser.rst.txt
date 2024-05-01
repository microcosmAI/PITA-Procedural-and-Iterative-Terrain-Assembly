Parser Module
=============

Overview
--------

The `parser` module in the PITA Algorithm framework is specifically designed for parsing object definitions and configurations from various sources, including YAML or JSON files. This module plays a crucial role in interpreting the complex configurations needed for simulating environments within the MuJoCo physics engine, transforming them into actionable specifications for object instantiation and manipulation.

Key Features
------------

- **Versatile Configuration Parsing**: Capable of interpreting and extracting detailed simulation parameters from configuration files, supporting a wide range of object properties and simulation settings.
- **Direct Mapping to Simulation Objects**: Translates parsed configurations into direct specifications for the creation and configuration of `MujocoObject` instances, ensuring a seamless transition from abstract definitions to physical entities in the simulation environment.
- **Support for Extensive Object Properties**: Accommodates a broad spectrum of object attributes, from basic physical properties like size and mass to more intricate settings such as material textures and dynamic behaviors.
- **Enhanced Simulation Customizability**: By providing detailed control over object and environment configurations, it allows researchers and developers to tailor simulations to their specific experimental needs, enhancing the utility and applicability of the PITA Algorithm.

Usage
-----

The Parser module is typically employed at the initial stages of simulation setup, where it reads and processes configuration files to establish the parameters for the simulation environment and its constituent objects:

1. **Load Configuration**: Configuration files are loaded into the parser, which extracts and interprets the defined parameters.
2. **Object Specification**: Based on the parsed information, specifications for each simulation object, including their properties and behaviors, are established.
3. **Environment Setup**: These specifications are then utilized to instantiate and configure objects within the MuJoCo simulation environment, laying the groundwork for simulation execution.

This process underscores the parser module's critical role in bridging the gap between high-level simulation design and low-level execution, facilitating the creation of richly detailed and highly customized simulation scenarios.

.. automodule:: pitapy.base.asset_parsing.parser
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
