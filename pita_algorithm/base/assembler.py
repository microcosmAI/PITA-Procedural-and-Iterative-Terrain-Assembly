import copy
import numpy as np
from shapely import geometry

from pita_algorithm.base.world_sites.area import Area
from pita_algorithm.base.asset_placement.validator import Validator
from pita_algorithm.base.world_sites.environment import Environment
from pita_algorithm.base.asset_parsing.mujoco_loader import MujocoLoader
from pita_algorithm.base.asset_placement.fixed_placer import FixedPlacer
from pita_algorithm.base.asset_placement.random_placer import RandomPlacer
from pita_algorithm.base.asset_placement.border_placer import BorderPlacer
from pita_algorithm.base.asset_placement.boundary_rule import BoundaryRule
from pita_algorithm.base.asset_placement.min_distance_rule import MinDistanceRule
from pita_algorithm.base.asset_placement.random_walk_distribution import (
    RandomWalkDistribution,
)
from pita_algorithm.base.asset_placement.circular_uniform_distribution import (
    CircularUniformDistribution,
)
from pita_algorithm.base.asset_placement.multivariate_normal_distribution import (
    MultivariateNormalDistribution,
)
from pita_algorithm.base.asset_placement.min_distance_mujoco_physics_rule import (
    MinDistanceMujocoPhysicsRule,
)
from pita_algorithm.base.asset_placement.multivariate_uniform_distribution import (
    MultivariateUniformDistribution,
)


class Assembler:
    """Assembles the environment."""

    def __init__(self, config_file: dict, xml_dir: str):
        """Constructor of the Assembler class.

        Parameters:
            config_file (dict): Config file containing user defined parameters
            xml_dir (str): String to xml-directory
        """
        self.config = config_file
        self.xml_dir = xml_dir

    def assemble_world(self) -> tuple[Environment, list[Area]]:
        """Assembles the world according to the users configuration.

        Returns:
            environment (Environment): Environment class instance
            areas (list[Area]): List of Area class instances
        """
        # Call mujoco loader to get dictionary of mujoco objects
        mujoco_loader = MujocoLoader(config_file=self.config, xml_dir=self.xml_dir)
        mujoco_objects_blueprints = mujoco_loader.get_mujoco_objects()

        # Duplicate blueprints for rule checking that can be manipulated
        # without changing the original
        mujoco_objects_rule_blueprints = {}

        for name, mujoco_object in mujoco_objects_blueprints.items():
            mujoco_object_copy = copy.deepcopy(mujoco_object)

            # If a free joint is present, replace it with a normal joint
            joint_list = mujoco_object_copy.mjcf_obj.worldbody.body[0].find_all(
                "joint", immediate_children_only=True
            )
            if joint_list:
                if joint_list[0].tag == "freejoint" or joint_list[0].type == "free":
                    joint_list[0].remove()
                    mujoco_object_copy.mjcf_obj.worldbody.body[0].add(
                        "joint", limited="false"
                    )
                # Else keep joint as it is -> suffices for collision detection
                else:
                    pass
            # If no joint is present, add a normal joint for collision detection
            else:
                mujoco_object_copy.mjcf_obj.worldbody.body[0].add("joint")
            mujoco_objects_rule_blueprints[name] = mujoco_object_copy

        # Parse size from the config
        size_range = self._get_randomization_parameters(
            config_dict=self.config["Environment"], keys=["size_range"]
        )

        if size_range is None:
            raise ValueError("No size range provided.")

        if isinstance(size_range[0][0], (float, int)):
            size = (
                list(
                    np.random.uniform(
                        low=size_range[0][0], high=size_range[0][1], size=1
                    )
                )
                * 2
            )

        else:
            # Drop outer tuple and list and merge dictionaries
            size_range_dict = {
                key: value
                for dictionary in size_range[0]
                for key, value in dictionary.items()
            }

            if not {"length_range", "width_range"}.issubset(
                set(size_range_dict.keys())
            ):
                raise ValueError("Both length_range and width_range must be specified.")

            else:
                size = []
                size.extend(
                    np.random.uniform(
                        low=size_range_dict["length_range"][0],
                        high=size_range_dict["length_range"][1],
                        size=1,
                    )
                )
                size.extend(
                    np.random.uniform(
                        low=size_range_dict["width_range"][0],
                        high=size_range_dict["width_range"][1],
                        size=1,
                    )
                )

        pretty_mode = self.config["Environment"]["Style"][0]["pretty_mode"]

        # Create environment
        environment = Environment(
            name="Environment1", size=(size[0], size[1], 0.1), pretty_mode=pretty_mode
        )

        # Create areas
        # As long as we only have one area we set its size to the one of the environment
        # TODO: set size and boundary with layout manager
        areas = []

        # TODO: Dynamically create areas according to config
        if self.config.get("Areas") is not None:
            for area_index, _ in enumerate(self.config["Areas"].items()):
                areas.append(
                    Area(
                        name=f"Area{area_index+1}",
                        size=(size[0], size[1], 0.1),
                        environment=environment,
                        boundary=None,
                    )
                )
        # TODO: Initialize multiple areas
        """for area_name, area_settings in self.config["Areas"].items():
            areas.append(Area(name=area_name, size=(10, 10, 0.1)))"""

        # Create Validators
        environment_validator = Validator(
            [
                MinDistanceMujocoPhysicsRule(distance=1.0),
                BoundaryRule(boundary=(size[0], size[1])),
            ]
        )

        global_validators = [
            environment_validator,
        ]

        area_validators = []
        if self.config.get("Areas") is not None:
            for area_index, (area_name, area_settings) in enumerate(
                self.config["Areas"].items()
            ):
                area_validators.append(
                    Validator(
                        [
                            MinDistanceMujocoPhysicsRule(distance=1.0),
                            BoundaryRule(boundary=(size[0], size[1])),
                        ]
                    )
                )

        # Border Placement
        border_config_dict = {}
        for dict_ in self.config["Environment"]["Borders"]:
            border_config_dict.update(dict_)
        has_border = border_config_dict["place"]
        BorderPlacer().add(
            environment=environment,
            mujoco_object_blueprint=mujoco_objects_blueprints["Border"],
            amount=4,
            has_border=has_border,
        )

        if has_border:
            # Add Border to map2D of environment validator
            global_validators[0].map_2D[mujoco_objects_blueprints["Border"].name] = [
                geometry.LineString(
                    [
                        [-size[0], -size[1]],
                        [-size[0], size[1]],
                        [size[0], size[1]],
                        [size[0], -size[1]],
                        [-size[0], -size[1]],
                    ]
                )
            ]

        # TODO: Maybe see if its possible to not loop over these item a second time for random placement
        # Fixed Coordinate Mujoco Object Placement - Environment level
        for object_name, object_settings in self.config["Environment"][
            "Objects"
        ].items():
            object_config_dict = {}
            for dict_ in object_settings:
                object_config_dict.update(dict_)

            (
                z_rotation_range,
                color_groups,
                size_groups,
                size_value_range,
                asset_pool,
            ) = self._get_randomization_parameters(
                config_dict=object_config_dict,
                keys=[
                    "z_rotation_range",
                    "color_groups",
                    "size_groups",
                    "size_value_range",
                    "asset_pool",
                ],
            )

            # Checks for coordinates and if they are present, place the object using the fixed placer
            for objects in object_settings:
                if "coordinates" in objects:
                    FixedPlacer().add(
                        site=environment,
                        mujoco_object_blueprint=mujoco_objects_blueprints[object_name],
                        mujoco_object_rule_blueprint=mujoco_objects_rule_blueprints[
                            object_name
                        ],
                        validators=global_validators,
                        amount=object_config_dict["amount"],
                        coordinates=objects["coordinates"],
                        z_rotation_range=z_rotation_range,
                        color_groups=color_groups,
                        size_groups=size_groups,
                        size_value_range=size_value_range,
                        asset_pool=asset_pool,
                        mujoco_objects_blueprints=mujoco_objects_blueprints,
                    )

        # Fixed Coordinate Mujoco Object Placement - Area level
        if self.config.get("Areas") is not None:
            for area_index, (area_name, area_settings) in enumerate(
                self.config["Areas"].items()
            ):
                for object_name, object_settings in area_settings["Objects"].items():
                    object_config_dict = {}
                    for dict_ in object_settings:
                        object_config_dict.update(dict_)

                    (
                        z_rotation_range,
                        color_groups,
                        size_groups,
                        size_value_range,
                        asset_pool,
                    ) = self._get_randomization_parameters(
                        config_dict=object_config_dict,
                        keys=[
                            "z_rotation_range",
                            "color_groups",
                            "size_groups",
                            "size_value_range",
                            "asset_pool",
                        ],
                    )

                    # Checks for coordinates and if they are present, place the object using the fixed placer
                    for objects in object_settings:
                        if "coordinates" in objects:
                            FixedPlacer().add(
                                site=areas[area_index],
                                mujoco_object_blueprint=mujoco_objects_blueprints[
                                    object_name
                                ],
                                mujoco_object_rule_blueprint=mujoco_objects_rule_blueprints[
                                    object_name
                                ],
                                validators=[
                                    area_validators[area_index],
                                ]
                                + global_validators,
                                amount=object_config_dict["amount"],
                                coordinates=objects["coordinates"],
                                z_rotation_range=z_rotation_range,
                                color_groups=color_groups,
                                size_groups=size_groups,
                                size_value_range=size_value_range,
                                asset_pool=asset_pool,
                                mujoco_objects_blueprints=mujoco_objects_blueprints,
                            )

        # Random Mujoco Object Placement - Environment level
        for object_name, object_settings in self.config["Environment"][
            "Objects"
        ].items():
            if "coordinates" not in [
                list(setting.keys())[0] for setting in object_settings
            ]:
                object_config_dict = {}
                for dict_ in object_settings:
                    object_config_dict.update(dict_)

                # Instantiate placer distribution and call random placer
                environment_random_distribution = MultivariateUniformDistribution(
                    parameters={
                        "low": [-environment.size[0], -environment.size[1]],
                        "high": [environment.size[0], environment.size[1]],
                    }
                )
                (
                    z_rotation_range,
                    color_groups,
                    size_groups,
                    size_value_range,
                    asset_pool,
                ) = self._get_randomization_parameters(
                    config_dict=object_config_dict,
                    keys=[
                        "z_rotation_range",
                        "color_groups",
                        "size_groups",
                        "size_value_range",
                        "asset_pool",
                    ],
                )
                RandomPlacer(distribution=environment_random_distribution).add(
                    site=environment,
                    mujoco_object_blueprint=mujoco_objects_blueprints[object_name],
                    mujoco_object_rule_blueprint=mujoco_objects_rule_blueprints[
                        object_name
                    ],
                    validators=global_validators,
                    amount=object_config_dict["amount"],
                    z_rotation_range=z_rotation_range,
                    color_groups=color_groups,
                    size_groups=size_groups,
                    size_value_range=size_value_range,
                    asset_pool=asset_pool,
                    mujoco_objects_blueprints=mujoco_objects_blueprints,
                )

        # Random Mujoco Object Placement - Area level
        if self.config.get("Areas") is not None:
            for area_index, (area_name, area_settings) in enumerate(
                self.config["Areas"].items()
            ):
                for object_name, object_settings in area_settings["Objects"].items():
                    # Get all keys from the 2d list of dictionaries
                    if "coordinates" not in [
                        list(setting.keys())[0] for setting in object_settings
                    ]:
                        object_config_dict = {}
                        for dict_ in object_settings:
                            object_config_dict.update(dict_)

                        # Instantiate placer distribution and call random placer
                        area_random_distribution = MultivariateUniformDistribution(
                            parameters={
                                "low": [-environment.size[0], -environment.size[1]],
                                "high": [environment.size[0], environment.size[1]],
                            }
                        )
                        (
                            z_rotation_range,
                            color_groups,
                            size_groups,
                            size_value_range,
                            asset_pool,
                        ) = self._get_randomization_parameters(
                            config_dict=object_config_dict,
                            keys=[
                                "z_rotation_range",
                                "color_groups",
                                "size_groups",
                                "size_value_range",
                                "asset_pool",
                            ],
                        )
                        RandomPlacer(distribution=area_random_distribution).add(
                            site=areas[area_index],
                            mujoco_object_blueprint=mujoco_objects_blueprints[
                                object_name
                            ],
                            mujoco_object_rule_blueprint=mujoco_objects_rule_blueprints[
                                object_name
                            ],
                            validators=[
                                area_validators[area_index],
                            ]
                            + global_validators,
                            amount=object_config_dict["amount"],
                            z_rotation_range=z_rotation_range,
                            color_groups=color_groups,
                            size_groups=size_groups,
                            size_value_range=size_value_range,
                            asset_pool=asset_pool,
                            mujoco_objects_blueprints=mujoco_objects_blueprints,
                        )

        # Add plane to environment, if pretty mode is enabled also add grid material
        if pretty_mode:
            environment.mjcf_model.worldbody.add(
                "geom",
                name="base_plane",
                type="plane",
                size=(size[0], size[1], 0.1),
                material="grid",
            )
        else:
            environment.mjcf_model.worldbody.add(
                "geom",
                name="base_plane",
                type="plane",
                size=(size[0], size[1], 0.1),
            )

        # Use global validator to plot the map layout
        global_validators[0].plot(env_size=environment.size)

        return environment, areas

    def _get_randomization_parameters(self, config_dict: dict, keys: list) -> tuple:
        """Reads the randomization parameters in config_dict for the given keys.

        Parameters:
            config_dict (dict): Contains information about world settings
            keys (list): List of keys to read from the config_dict

        Returns:
            tuple: Tuple containing the values for the given keys in the order they were passed
        """
        # Initialize default values
        default_values = [None] * len(keys)

        # Loop over keys and update default values
        for i, key in enumerate(keys):
            if key in config_dict:
                default_values[i] = config_dict[key]

        return tuple(default_values)
