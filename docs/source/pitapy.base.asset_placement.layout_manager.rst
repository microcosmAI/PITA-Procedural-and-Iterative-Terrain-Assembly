LayoutManager Module
====================

Overview
--------

The `LayoutManager` class is instrumental in orchestrating the layout of Area-sites within the PITA Algorithm framework, especially when multiple areas are present in the simulation environment. It calculates and applies a tiling layout based on the environment's dimensions and the specified number of areas, ensuring an optimal utilization of space and facilitating detailed control over the simulation's spatial organization.

YAML Configuration and Flexibility
----------------------------------

The `LayoutManager` seamlessly integrates with YAML configuration files, allowing users to specify the environment dimensions, the desired number of areas, and whether to visualize the layout through a bird's-eye view 2D map. This feature underscores the framework's commitment to flexibility and user configurability:

- **Environment Dimensions**: Define the length and height of the simulation environment.
- **Area Count**: Specify the number of areas into which the environment should be divided.
- **Visualization**: Opt-in for a graphical representation of the calculated layout to assist in planning and debugging.

Key Features
------------

- **Automatic Tiling Calculation**: Dynamically calculates an efficient tiling layout that optimally divides the environment according to specified parameters.
- **Visualization Support**: Offers the capability to plot the resulting layout, providing immediate visual feedback on the division of space.
- **Configurable via YAML**: Parameters for layout management can be easily defined in a YAML configuration file, enhancing ease of use and accessibility.

Usage
-----

To leverage the `LayoutManager` in your simulation setup:

1. Instantiate the `LayoutManager` with the environment's dimensions, the number of areas, and a flag indicating whether to plot the layout.
2. Call the `tiling` method to calculate the layout based on the provided parameters.
3. Optionally, use the `plot_tiling_boundaries` method to generate a visual representation of the calculated layout.

Remember, you can do the specifics of your environment from the config.yml

.. automodule:: pitapy.base.asset_placement.layout_manager
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
