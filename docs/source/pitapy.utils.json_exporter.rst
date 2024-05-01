JSONExporter Module
==================

.. module:: pitapy.utils
   :synopsis: Exports environment and area object information to a JSON file.

The `JSONExporter` class serves as a utility within the PITA Algorithm framework to serialize and export the setup of environments and their respective areas, including all associated objects and configurations, into a JSON format. This functionality is crucial for documenting simulation setups, sharing configurations, or even re-initializing environments with specific settings.

Usage
-----

The `JSONExporter` class offers a static method `export` that takes as input the path for the export file, the configuration dictionary, the environment instance, and a list of area instances. This method processes these inputs to generate a comprehensive JSON document detailing the configurations and objects within the environment and its areas.

.. autoclass:: pitapy.utils.JSONExporter
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: pitapy.utils.json_exporter
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
