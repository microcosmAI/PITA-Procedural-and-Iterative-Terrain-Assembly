.. Peter Algorithm documentation master file, created by
   sphinx-quickstart on Tue Apr 11 15:59:18 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Peter Algorithm's documentation!
===========================================

Welcome to the Peter Algorithm Documentation Landing Page!

Peter's Algorithm is an automated, modular, and randomized world generator designed specifically for reinforcement learning (RL) environments that are built with MuJoCo. 
The algorithm simplifies and speeds up the process of creating environments while addressing the problem of overfitting commonly encountered in RL.

The Peter Algorithm is based on a "Toolbox" principle that allows for a high level of customization. 
Users can specify the size of the world, divide it into sub-areas, and determine the number and type of objects to be placed in the environment. 
The algorithm also includes an inbuilt validation feature that ensures fixed or randomly placed objects do not collide with each other.

Once the algorithm completes its generation process, it produces a single .xml file that can be loaded into MuJoCo and serves as the simulation world for the RL agents. 
Users can easily configure the algorithm using a simple yml file without needing a strong programming background.

This project is part of a university course called "Emergent Behaviors in a Multi-Agent System with Reinforcement Learning" (EBIMAS).


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Peter Algorithm Docs

   API Reference <modules>
   Open Issues <https://github.com/microcosmAI/s.peters_algorithm/issues>
   Our GitHub <https://github.com/microcosmAI/s.peters_algorithm>
  
.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Guides

   Installation Guide <install>
   Usage Guide <usage>


.. note::

   This project is under active development and therefore the algorithm and its documentation are subject to change.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
