AbstractSite Module
==================

Overview
--------

The `AbstractSite` class defines a standard interface for all site entities within the PITA Algorithm framework. Serving as a base class for specific types of sites, such as environments or distinct areas within a simulation, it mandates the implementation of essential methods and properties that govern object management and site characteristics.

Key Features
------------

- **Object Management**: Provides abstract methods for adding and removing MuJoCo objects, enabling dynamic manipulation of the simulation's entities.

- **Site Identification**: Includes abstract properties for getting and setting the site's name, allowing easy identification and differentiation of sites.

- **Spatial Characteristics**: Defines abstract properties for accessing the site's size and its corresponding MuJoCo XML model, supporting spatial calculations and physical simulations.


.. automodule:: pitapy.base.world_sites.abstract_site
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
