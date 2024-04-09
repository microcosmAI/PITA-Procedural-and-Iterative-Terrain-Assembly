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
To verify that PITA is installed correctly, you can run a simple test or a sample project included in the repository, uses complex.config.yml by default. Navigate to the pita_algorithm subfolder and run:

.. code-block:: bash

    python pita.py

Configuration and Usage
-----------------------

The `config.yml` file is central to configuring your environment generation settings with PITA. It enables the specification of various parameters, including the size of the environment, placements of objects, features of the terrain, rules for simulation, among others.

Below is an example configuration that illustrates the inclusion of an agent within the environment and the definition of an area containing a ball object:

.. code-block:: yaml

    Environment:
      size_range:
        - length_range: [200, 300]  # Defines the variability in environment length.
        - width_range: [300, 400]   # Defines the variability in environment width.
      Style:
        - pretty_mode: True         # Enables enhanced visual features.
      random_seed: 42               # Ensures reproducibility of simulation setups.

      Objects:
        Agent:
          - xml_name: "Agent.xml"   # Specifies the XML file defining the Agent's characteristics.
          - amount: 1               # Sets the number of Agents to be placed.
          - coordinates: [50, 50, 0] # Directly places the Agent at specified coordinates.

    Areas:
      Area1:
        Objects:
          Ball:
            - xml_name: "Ball.xml"  # Specifies the XML file defining the Ball's characteristics.
            - amount: [1, 2]        # Allows for 1 to 2 Balls to be placed within Area1.

In this configuration:

- `size_range` sets the dimensions of the overall environment, ensuring a dynamic and variable space for simulation activities.
- `pretty_mode` when set to True, enhances the visual appeal of the generated environment, making it more suitable for presentations or detailed analysis.
- `random_seed` is used to guarantee the consistency of the environment generation process across different runs, aiding in reproducibility.
- The `Objects` section within `Environment` defines individual entities like agents and their properties, including appearance (via `xml_name`), quantity (`amount`), and placement (`coordinates`).
- The `Areas` section allows for the segmentation of the environment into distinct zones, each with its own set of objects and configurations. In the example, `Area1` contains a variable number of balls as specified.

This detailed approach to configuration offers significant flexibility, allowing users to craft unique and varied simulation environments tailored to their specific research or development needs. For a comprehensive overview of all configuration options and their impact on the environment generation process, refer to the full PITA config.yml documentation page.

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