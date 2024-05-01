Distributions in PITA Algorithm
===============================

Overview
--------

The `distributions` package is a vital component of the PITA Algorithm, offering a versatile set of strategies for object placement within simulation environments. These strategies allow for the dynamic and realistic arrangement of objects, catering to a wide array of simulation needs and enhancing the environmental complexity crucial for in-depth research and analysis.

Distribution Strategies
-----------------------

This package includes a variety of distribution classes, each tailored for specific placement patterns and simulation requirements:

- **Multivariate Normal Distribution**: Utilizes mean values and a covariance matrix to define a Gaussian distribution for object placement. Ideal for simulations requiring naturally clustered or dispersed objects, with support for correlation among variables.

- **Multivariate Uniform Distribution**: Offers a straightforward, uniform placement of objects across the simulation space. This distribution is perfect for evenly spreading objects, ensuring uniform object density and distribution.

- **Random Walk Distribution**: Simulates a random walk for object placement, creating paths or trails that mimic natural movement patterns across a 2D plane. This strategy adds a dynamic, unpredictable element to simulations.

- **Circular Uniform Distribution**: Places objects uniformly within a circular area, centered around a specific point. This strategy is suited for scenarios that demand radial symmetry in object distribution.

Implementing Distribution Strategies
------------------------------------

Integrating these distribution strategies into your simulation involves:

1. **Selection**: Choose the distribution strategy that best fits your simulation's objectives and environmental setup.
2. **Configuration**: Instantiate the chosen distribution class with the necessary parameters, such as mean and covariance for Gaussian distributions, or step sizes and bounds for a random walk.
3. **Integration**: Apply the distribution strategy during the object placement phase, using it to determine the spatial arrangement of objects within your environment.

By leveraging the diverse array of distribution strategies offered by the `distributions` package, simulations can achieve a higher degree of environmental realism and complexity. This facilitates more nuanced research outcomes and provides a robust foundation for exploring a wide range of scientific questions.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   implementation_details
   example_use_cases


.. automodule:: pitapy.base.asset_placement.distributions
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

Submodules
----------

.. toctree::
   :maxdepth: 5

   pitapy.base.asset_placement.distributions.abstract_placer_distribution
   pitapy.base.asset_placement.distributions.distribution_collection
