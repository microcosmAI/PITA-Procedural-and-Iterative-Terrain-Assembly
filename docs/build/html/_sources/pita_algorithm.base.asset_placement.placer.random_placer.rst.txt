RandomPlacer Class
==================

Overview
--------

The `RandomPlacer` class, inheriting from `AbstractPlacer`, introduces a method for placing objects randomly within the environment or specific areas, making use of distribution strategies to guide the randomness. This class is crucial for simulations that benefit from stochastic object arrangements, providing a means to explore diverse scenarios within a controlled simulation framework.

Functionalities
---------------

- **Random Object Placement**: Enables the placement of objects at random coordinates within the simulation environment, leveraging specified distribution strategies to control the randomness.

- **Integration with Distribution Strategies**: Utilizes a variety of distribution strategies, allowing objects to be placed according to complex patterns such as uniform, Gaussian, or custom distributions defined by the user.

- **Property Customization**: Supports the randomization of object properties, including color, size, and rotation, before placement, enhancing the dynamism and visual diversity of the simulation.

- **Retry Mechanism**: Implements a retry mechanism that attempts to place each object up to a predefined maximum number of tries, ensuring that objects are placed within valid locations according to the validators.

Usage
-----

Initialization of the `RandomPlacer` requires no parameters beyond those inherited from `AbstractPlacer`. The placement process involves specifying the site for placement, the object blueprint, validators to ensure valid placement, and the distribution strategy, among other customizable properties.

.. automodule:: pita_algorithm.base.asset_placement.placer.random_placer
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
