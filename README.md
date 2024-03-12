# PITA
The PITA algorithm acts as an automatic modular randomized world generator

## Installation Instructions

These instructions are for setting up the algorithm's environment and dependencies.

```shell
conda create --name PITA python=3.10.11
conda activate PITA
```

```shell
git clone https://github.com/microcosmAI/s.peters_algorithm.git # clone
cd s.peters_algorithm
pip install -r requirements.txt # install 
```

## Code Examples
This section provides a simple command to run the algorithm.

```shell
python pita_algorithm/pita.py 
```
The script uses the configuration example yml files in the examples/config_files directory and generates .json and .xml files in the export directory.

`.xml` file created by `pita.py` in the export directory could be used for the Mujoco environment.   

### Example for running on Mujoco

To run the simulation on Mujoco, use the appropriate script for your operating system. Replace [YOUR_OS] in the command below with osx, linux, or win

```shell
sh run_[YOUR_OS].sh 
```

## Licensing
