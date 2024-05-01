# PITA (Procedural and Iterative Terrain Assembly)
![pixlr_banner](./static/banner.png)

Welcome to the documentation for PITA (Procedural and Iterative Terrain Assembly), a framework designed to generate dynamic and customizable environments for **reinforcement learning (RL) in MuJoCo**. PITA serves as a valuable tool for creating varied simulation environments, helping to mitigate overfitting in AI systems by providing diverse training scenarios.

Introduction
------------
<img align="right" width="150" src="./static/pitabot.png">

AI systems require exposure to a variety of environments to develop robust and adaptable behaviors. Static, unchanging environments can lead to overfitting, where AI agents perform well in familiar scenarios but struggle with any variation. PITA addresses this challenge by generating multiple variations of the same environment, in which the properties and positions of objects can be altered. This is achieved through randomization, over which the user has control, allowing for a more dynamic and adaptable testing scenario.

Core Features
---------------

- **YAML Configuration**: Simplifies the environment setup process through YAML configuration files, eliminating the need for direct coding and making the system accessible to users with minimal programming experience.

- **XML Input**: The system uses XML files as inputs, enabling users to supply custom assets by passing the directory of the xmls to PITA.

- **Fine-Grained Configuration Control**: Offers detailed control over the placement and properties of assets with the additional capability to randomize these aspects as required.

- **Property Randomization**: Offers the ability to randomize various properties of every asset, including position, number, colors, sizes, and z-axis rotation.

- **Adjustable Environment Sizes**: Supports static variable dimensions for the base environment while also including the option to randomize length and height which results in different boundary dimensions for every variation of the base environment.

- **Segmented Environmental Areas**: Allows the division of the overall environment into multiple equal-sized areas. Object behavior, such as position randomization, is then based on the area they are positioned in.

- **Distribution-Based Randomization**: Implements position randomization through statistical distributions, providing users with the option to select specific distribution models for each asset to achieve desired randomness effects.

- **Runtime Validation of Asset Positioning**: Ensures that all assets are correctly positioned without overlaps through validation at run-time.

- **Placement Rules**: Allows setting specific rules for asset placement, such as maintaining a minimum distance between objects.

- **Diverse Asset Pool**: Enables the definition of an asset pool, allowing selection from various assets of a similar style (e.g., "Tree.xml", "Tree_Birch.xml", "Tree_Maple.xml").

- **JSON Output**: Generates a JSON file detailing information about the objects within the environment, providing a structured output that can be used for the environment dynamics.


Why PITA?
---------

PITA offers several advantages for the development and training of RL systems:

- **Aimed for RL and MuJoCo**: PITA is specifically designed for reinforcement learning scenarios using the MuJoCo framework, known for its complex interactions. PITA simplifies the use of MuJoCo by allowing users to integrate custom assets and define settings through a straightforward configuration file, effectively streamlining the complexity of the environment setup.
- **Facilitates Generalization**: Mitigates overfitting by generating varied environments of the same setup in order for the agent to develop a deeper understanding of the environment and the task at hand.
- **Fast Multi-Environment Creation**: The easy-to-use configuration system speeds up the process of environment generation.

PITA provides a framework for the procedural and iterative assembly of training environments, designed to support reinforcement learning research. It offers researchers and developers the tools needed to construct diverse and challenging scenarios, aiding in the development of AI agents that can perform well across different tasks or domains.

## 1) Installation
In order to get started, simply install the package

```bash
pip install pitapy
```

## 2) Quick Start

Import the PITA class from the package and run it.

```shell
from pitapy.pita import PITA


PITA().run()
```

This script uses the default values within the package:
```shell
random_seed=None
config_path="examples/config_files/complex-config.yml"
xml_dir="examples/xml_objects"
export_path="export/test"
```

## 3) Designing the configuration file 

This is an example of a simple configuration file to start with PITA. For further details on 'how to design your own configuration file' please visit our documentation by opening
"docs/build/html/index.html" in your browser.
```
Environment:
  size_range: [100, 100]

  random_seed: 42

  Style:
    - pretty_mode: False

  Borders:
    - xml_name: "Border.xml"
    - place: True
    - tags: ["Border"]

  Objects:
    Tree01:
      - xml_name: "Tree01.xml"
      - amount: [2, 2]

    Agent:
      - xml_name: "BoxAgent.xml"
      - amount: 2
      - coordinates: [ [10, 10, 3], [10, 30, 3] ]

Areas:
  Area1:
    Objects:
      Tree02:
        - xml_name: "Tree02.xml"
        - amount: [2, 2]
        - tags: ["Tree"]
```

## MicrocosmAI
The development of PITA is part of the "Emergent Behaviors in a Multi-Agent System with Reinforcement Learning" study project conducted by the MicrocosmAI research group at the University of Osnabrück.

## Outlook
As PITA is an active component of the ongoing research project, it will continue to evolve to align with the requirements of specific tasks. The development of additional features will be guided by the insights gained from the research activities associated with the project.

## License
3-Clause BSD

Copyright 2024 MicrocosmAI

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
