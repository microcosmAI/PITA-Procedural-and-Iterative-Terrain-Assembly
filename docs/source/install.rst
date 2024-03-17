PITA Algorithm: A Comprehensive Guide
=====================================

.. contents::
   :local:
   :depth: 2

Introduction
------------
The Procedural Iterative Terrain Algorithm (PITA) enables the generation of complex and detailed environments for simulations and interactive applications. This guide provides detailed instructions on installing PITA, configuring your environment, and beginning to generate your own simulated worlds.

Installation Guide
------------------

Prerequisites
~~~~~~~~~~~~~
Before installing the PITA algorithm, ensure that you have the following prerequisites installed on your system:

- Python 3.6 or higher
- pip (Python package manager)
- Virtual environment (optional but recommended for isolating Python environments)

Step 1: Clone the PITA Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First, clone the PITA repository from GitHub to your local machine using Git. If you do not have Git installed, download and install it from `https://git-scm.com/`.

.. code-block:: bash

    git clone https://github.com/microcosmAI/pita.git
    cd pita-repository

Step 2: Create a Virtual Environment (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It's recommended to use a Python virtual environment to avoid conflicts with other Python projects on your system.

.. code-block:: bash

    python3 -m venv pita-env
    source pita-env/bin/activate

*Note: On Windows, the activation command is* `pita-env\Scripts\activate`.

Step 3: Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Inside the cloned directory, install the required Python packages using pip.

.. code-block:: bash

    pip install -r requirements.txt

Step 4: Verify Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~
To verify that PITA is installed correctly, you can run a simple test or a sample project included in the repository, uses complex.config.yml by default. Navgate to the pita_algorithm subfolder and run:

.. code-block:: bash

    python pita.py


Step 5: Deactivation and Cleanup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When you're done working with PITA, you can deactivate the virtual environment and, if necessary, delete it.

Deactivate the virtual environment:

.. code-block:: bash

    deactivate

To remove the virtual environment entirely, simply delete the `pita-env` directory.

Configuration and Usage
-----------------------
Refer to the `config.yml` file for configuring your environment generation settings. This YAML file allows you to specify parameters such as the environment size, object placements, terrain features, rules for the simulation and other behaviors.

For a more deatailed config, see the PITA config.yml page. But as a samlpe here, 

.. _configuration_section:


.. code-block:: yaml

    Environment:
      size_range:
        - length_range: [200, 300]
        - width_range: [300, 400]
      Style:
        - pretty_mode: True
      random_seed: 42

For each parameter in `config.yml`:

- `size_range`: Defines the dimensions of the environment.
- `pretty_mode`: A boolean that toggles enhanced visual features for the generated environment.
- `random_seed`: Ensures reproducibility by setting a seed for random number generation.

Refer to the full PITA config.yml page for detailed explanations of each configuration option and how they influence the environment generation process.


Customization and Extensions
-----------------------------

PITA is designed with customization in mind. Here’s how you can adapt it to fit your needs better:

- **Modifying Configuration Files:** Adjust parameters in the `config.yml` file to fine-tune the algorithm’s behavior.
- **Extending the Code:** Implement additional features or modifications by extending the base classes provided. It's built with a ToolBox paradigm and you should be able to easily tailor it further with features if not available. 

Troubleshooting
---------------

If you encounter issues while using the PITA Algorithm, consider the following troubleshooting steps:

- Ensure all dependencies are correctly installed and up-to-date.
- Verify your configuration files are correctly formatted and located in the expected directory.
- Consult the algorithm’s documentation for guidance on specific error messages or behavior.

Support and Contributions
-------------------------

For further support, or to contribute to the PITA Algorithm project, please do those via the project github.

This guide aims to provide a foundational understanding of how to set up, configure, and utilize the Peter Algorithm effectively. By following these instructions, users can harness the full potential of the algorithm for their specific applications or research.


Conclusion
----------
With the PITA algorithm installed and configured, you're now ready to generate complex and iterative environments. Experiment with different settings in the `config.yml` file to explore the full range of capabilities offered by PITA.