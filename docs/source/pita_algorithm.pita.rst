PITA.py and Execution Script
===============================

.. module:: pita_algorithm.pita
   :synopsis: Main class and script for executing the PITA algorithm.

The `PITA` class orchestrates the execution of the PITA algorithm, leveraging the framework's capabilities to assemble simulation environments, manage objects, and export the configured world to XML and JSON formats. This class facilitates the integration of user-defined configurations and object models into a coherent simulation environment.

PITA Class
----------

.. autoclass:: pita_algorithm.pita.PITA
   :members:
   :undoc-members:
   :show-inheritance:

The `PITA` class provides the `run` method, which performs the primary functions necessary to configure and export the simulation environment based on user specifications.

Usage
-----

To execute the PITA algorithm, the `PITA` class is instantiated and its `run` method is invoked with appropriate parameters, including the random seed, configuration path, XML directory, export path, and an optional plot flag.

The class can be directly utilized within Python scripts or integrated into larger simulation frameworks to dynamically generate and manage simulation environments.

Main Function
-------------

The `main` function serves as the command-line entry point for executing the PITA algorithm, using Typer to parse command-line options.

.. autofunction:: pita_algorithm.pita.main

Command-Line Execution
----------------------

The PITA algorithm can be executed from the command line, providing flexibility in specifying the configuration file, XML object directory, export path, and other options directly as command-line arguments.

.. code-block:: console

   $ python -m pita_algorithm.pita --config_path="path/to/config.yml" --xml_dir="path/to/xmls" --export_path="path/to/export" --plot

This example demonstrates running the PITA algorithm with specified configuration and XML directories, an export path for the generated files, and an optional plot flag to visualize the simulation environment.

Best Practices
--------------

- **Configuration Management**: Ensure that the configuration YAML file accurately reflects the desired simulation setup, including environments, objects, and rules.


.. note:: The `PITA` class and its command-line interface provide a powerful tool for configuring, assembling, and exporting simulation environments within the PITA Algorithm framework. By streamlining the process of simulation setup, the PITA algorithm enhances the efficiency and flexibility of simulation-based research and development projects.
