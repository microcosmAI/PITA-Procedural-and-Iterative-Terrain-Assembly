Distribution Collection Module
==============================

Overview
--------

The `distributions` package offers a suite of distribution strategies for object placement within the PITA Algorithm framework. These strategies enable the simulation of diverse environmental layouts by dictating how objects are spatially arranged. From multivariate normal distributions to random walks and circular uniform distributions, each class provides unique placement patterns to enhance the complexity and realism of simulation scenarios.

Multivariate Normal Distribution
--------------------------------

Defined by mean values and a covariance matrix, the `MultivariateNormalDistribution` class allows for the placement of objects according to a Gaussian distribution. This strategy is versatile, supporting both correlated and uncorrelated variables, and enables the rotation and scaling of distributions through the covariance matrix.

Multivariate Uniform Distribution
---------------------------------

The `MultivariateUniformDistribution` class offers a simple yet effective approach to distributing objects uniformly across a defined 2D space. With customizable lower and upper bounds, this distribution ensures objects are evenly spread, suitable for scenarios requiring uniform object density.

Random Walk Distribution
------------------------

Simulating a random walk, the `RandomWalkDistribution` class places objects based on a series of steps in random directions. This strategy is ideal for creating paths or trails of objects within the environment, mimicking natural or random movements over a 2D plane.

Circular Uniform Distribution
-----------------------------

Focusing on radial symmetry, the `CircularUniformDistribution` class distributes objects uniformly within a circular area. This distribution is particularly useful for scenarios where objects need to be centered around a point or distributed within circular bounds, offering a controlled yet randomized layout.

Usage
-----

To employ these distribution strategies within your simulation setup:

1. Choose the appropriate distribution class based on your environmental layout and object placement needs.
2. Instantiate the class with relevant parameters, such as mean and covariance for a Gaussian distribution, or step size and bounds for a random walk.
3. Integrate the distribution instance with your object placer logic, applying the distribution strategy during the simulation's object placement phase.

By leveraging these diverse distribution strategies, developers can create richly detailed simulation environments, suitable for a wide range of research applications and experimental designs.

.. automodule:: pita_algorithm.base.asset_placement.distributions.distribution_collection
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
