===================================================
Comprehensive Guide to PITA Algorithm's config.yml
===================================================

.. image:: screenshot.png
  :width: 400
  :alt: Alternative text

The PITA Algorithm's ``config.yml`` file allows users to meticulously define the simulation environment, including the characteristics and behaviors of objects within. This guide delves into each configurable option, ensuring users can fully leverage the algorithm's capabilities.

Environment Configuration
-------------------------

The environment section is pivotal, setting the stage for your simulation.

- **size_range**: Dictates the dimensions of the environment, crucial for spatial dynamics. It consists of ``length_range`` and ``width_range``, each defined by a list indicating minimum and maximum values. This range offers flexibility in environment size, accommodating various simulation scales.

  .. code-block:: yaml

    size_range:
      - length_range: [200, 300]  # Environment length between 200 and 300 units.
      - width_range: [300, 300]   # Environment width fixed at 300 units.

- **Style**: Influences the aesthetic aspects of the simulation. The ``pretty_mode`` flag enables a more visually appealing environment, potentially enhancing visualization for presentations or analysis.

  .. code-block:: yaml

    Style:
      - pretty_mode: False  # Toggle for stylized rendering.

- **random_seed**: A deterministic approach to randomness, ensuring reproducibility of simulation outcomes. Specifying a seed value guarantees that random processes within the simulation (e.g., object placements or behaviors) can be replicated precisely.

  .. code-block:: yaml

    random_seed: 42  # Seed for random number generation.

- **Headlight**: Configures the simulation's lighting, directly affecting the visual perception of the environment. Parameters include ``active`` to toggle the light, ``diffuse`` for diffuse light color, and ``ambient`` for ambient light color, enhancing realism or focusing attention.

  .. code-block:: yaml

    Headlight:
      - active: 0             # 0 or 1 to deactivate or activate the headlight.
      - diffuse: [0.4, 0.4, 0.4]  # RGB diffuse light color.
      - ambient: [0.1, 0.1, 0.1]  # RGB ambient light color.

- **Rules**: Enforces constraints and behaviors across the environment. Includes global rules like ``MinAllDistance`` for minimum separation between objects, ``Boundary`` to confine objects within a specified perimeter, and ``Height`` to ensure objects remain above a defined ground level.

  .. code-block:: yaml

    Rules:
      - MinAllDistance:
          - distance: 1.0  # Minimum distance between all objects.
      - Boundary:           # Ensures objects stay within environment bounds.
      - Height:
          - ground_level: 0.0  # Minimum height (elevation) of objects.

- **Borders**: Specifies properties and placements of borders around the environment, potentially used to delineate areas or create barriers.

  .. code-block:: yaml

    Borders:
      - xml_name: "Border.xml"  # Reference to the border object's XML file.
      - place: True             # Toggle to place or omit borders.
      - tags: ["Border"]        # Tags for categorization or identification.

Objects Configuration
---------------------

Defines the properties and behaviors of each object type within the environment.

- **Agent**, **Ball**, **Tree**, **Stone**, **Apple**: This section allows detailed configuration for various object types, such as appearance, quantity, and physical properties. 

  .. code-block:: yaml

    Objects:
      Agent:
        - xml_name: "Agent.xml"  # XML file defining the object's appearance and properties.
        - amount: [1, 1]         # Specifies the exact or range of quantity.
        - distribution:          # Defines the spatial distribution within the environment.
            - name: "MultivariateNormalDistribution"  # Distribution type.
            - mean: [20, 20]     # Distribution mean for positioning.
            - cov: [[100, 0], [0, 100]]  # Covariance matrix for distribution spread.
        - z_rotation_range: [-180, 180]  # Range for random rotation along the Z-axis.
        - tags: ["Agent"]        # Tags for categorization or further specification.

Each object configuration can include:
- ``xml_name``: Reference to the XML file defining the object's appearance and physics properties.
- ``amount``: The quantity of objects to place, either as a fixed number or a range.
- ``distribution``: Spatial distribution parameters, influencing how objects are scattered or positioned within the environment.
- ``z_rotation_range``: Range of allowed rotation around the Z-axis, adding randomness to object orientation.
- ``color_groups`` and ``size_groups``: Define how objects are grouped by color and size, allowing for variation and categorization within the simulation.
- ``size_value_range``: Specifies the range of sizes for object scaling, enhancing the diversity of object appearances.
- ``tags``: A list of identifiers for object categorization, useful for applying specific behaviors or rules.

**Color Groups and Size Groups**

The ``color_groups`` and ``size_groups`` parameters, combined with ``size_value_range``, offer a nuanced approach to diversifying the visual characteristics of objects within your environments.

- **color_groups**: Defines how objects are grouped based on color, promoting visual diversity. Objects are randomly assigned colors from a predefined pool, with the specified group size determining how many objects share the same color.

- **size_groups**: Functions similarly to color groups but focuses on the scale of objects. Within the defined ``size_value_range``, objects are scaled to introduce size variability. The group size indicates the number of objects sharing the same size.

**Example**

.. code-block:: yaml

    Ball:
      - xml_name: "Ball.xml"
      - amount: 5
      - color_groups: [2, 3]
      - size_groups: [2, 3]
      - size_value_range: [0.5, 1.5]

In the example above, 5 balls are introduced with 2 to 3 members in each color and size group. Each group of balls shares the same color and size, with sizes randomly chosen between 0.5 to 1.5 times their original scale.


Areas Configuration
-------------------

Defines sub-sections within the environment, each with its own set of rules and objects.

- **Area1**, **Area2**, etc.: Each area is uniquely configured to simulate different conditions or settings within the same environment.

  .. code-block:: yaml

    Areas:
      Area1:
        Rules:
          - MinAllDistance:
              - distance: 1.0  # Minimum distance between objects specifically in Area1.
          - Boundary:           # Ensures objects in Area1 stay within specified bounds.
          - Height:
              - ground_level: 0.0  # Sets a specific ground level for Area1.

        Objects:
          Tree:
            - xml_name: "Tree.xml"
            - amount: [6, 10]   # Specifies the quantity range of trees in Area1.
            - z_rotation_range: [0, 90]  # Limit rotation of trees within a 90-degree range.
            - color_groups: [2, 4]  # Defines color groupings for trees.
            - size_groups: [2, 3]   # Sets size groupings for trees, affecting their scale.
            - size_value_range: [1, 2]  # Dictates the range of sizes for tree scaling.
            - distribution:
                - name: "CircularUniformDistribution"  # Distribution type for object placement.
                - loc: 28
                - scale: 50
            - tags: ["Tree"]    # Tags for further categorization or identification within Area1.

      Area2:
        # Similar structure as Area1, but with different configurations to represent another part of the environment.

The configuration for each area includes:
- ``Rules``: Similar to the environment rules but applied locally within an area.
- ``Objects``: Detailed configurations for each object type specific to the area, including distribution types and parameters tailored to create desired spatial arrangements.


Other Features in ``config.yml``
-----------------------------------

**Fixed and Random Amount with Coordinates**

- **Fixed Amount**: Specifying a fixed quantity necessitates defining the exact placement of each object through the ``coordinates`` parameter.

- **Relative Coordinates**: Using relative coordinates, such as ``[0.5, 0.5, 0]``, positions an object relative to its environment or area, based on percentages. Here, ``[0.5, 0.5, 0]`` centers the object.

**Example**

.. code-block:: yaml

    Stone:
      - xml_name: "Stone.xml"
      - amount: 1
      - coordinates: [0.5, 0.5, 0]  # Centers the stone within the environment.

**Listing of Available Rules and Distributions**

This section outlines the rules and distributions available for use, along with their parameters:

**Rules**:

- ``MinAllDistance``: Maintains a minimum distance among all objects.
  - ``distance``: Specifies the minimum distance.
- ``Boundary``: Ensures object confinement within predetermined bounds.
- ``Height``: Establishes a minimum height for object placement.
  - ``ground_level``: Dictates the ground level height.

**Distributions**:

- ``MultivariateNormalDistribution``: Arranges objects according to a normal distribution.
  - ``mean``, ``cov``: Defines the mean and covariance matrix of the distribution.
- ``CircularUniformDistribution``: Evenly distributes objects within a circular area.
  - ``loc``, ``scale``: Central point and radius of the circle.
- ``RandomWalkDistribution``: Spreads objects following a random path from a starting location.
  - ``step_size_range``, ``bounds``: Determines the step size range and movement boundaries.

**Asset Pool**

- **asset_pool**: Facilitates random selection from a set of assets for each object instance, enhancing environment variety.

**Example**

.. code-block:: yaml

    Tree:
      - xml_name: "Tree.xml"
      - amount: [1, 2]
      - asset_pool: ["Tree.xml", "Tree_Birch.xml", "Tree_Ahorn.xml"]

By introducing an asset pool, each tree (within the specified amount range) randomly selects its model from the provided asset options, potentially rendering each instance unique.

Conclusion
----------

This comprehensive guide to the PITA Algorithm's ``config.yml`` file highlights the depth and flexibility of simulation configuration. By understanding and utilizing these options, users can create intricate and varied simulation environments, tailored to their specific research, development, or presentation needs.
