import copy
import numpy as np
from shapely import geometry
from pita_algorithm.base.world_sites.area import Area
from pita_algorithm.base.asset_placement.validator import Validator
from pita_algorithm.base.world_sites.environment import Environment
from pita_algorithm.base.asset_parsing.mujoco_loader import MujocoLoader
from pita_algorithm.base.asset_placement.fixed_placer import FixedPlacer
from pita_algorithm.base.asset_placement.random_placer import (
    RandomPlacer,
    Placer2DDistribution,
)
from pita_algorithm.base.asset_placement.border_placer import BorderPlacer
from pita_algorithm.base.asset_placement.boundary_rule import BoundaryRule
from pita_algorithm.base.asset_placement.min_distance_rule import MinDistanceRule
from pita_algorithm.utils.multivariate_uniform_distribution import MultivariateUniform
from pita_algorithm.base.asset_placement.min_distance_mujoco_physics_rule import (
    MinDistanceMujocoPhysicsRule,
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
        self.mujoco_objects_blueprints = None
        self.mujoco_objects_rule_blueprints = None

    def get_object_blueprints(self):
        """Creates and manipulates the mujoco objects blueprints"""
        mujoco_loader = MujocoLoader(config_file=self.config, xml_dir=self.xml_dir)
        self.mujoco_objects_blueprints = mujoco_loader.get_mujoco_objects()

        self.mujoco_objects_rule_blueprints = {}
        for name, mujoco_object in self.mujoco_objects_blueprints.items():
            mujoco_object_copy = copy.deepcopy(mujoco_object)
            joint_list = mujoco_object_copy.mjcf_obj.worldbody.body[0].find_all(
                "joint", immediate_children_only=True
            )
            if joint_list:
                if joint_list[0].tag == "freejoint" or joint_list[0].type == "free":
                    joint_list[0].remove()
                    mujoco_object_copy.mjcf_obj.worldbody.body[0].add(
                        "joint", limited="false"
                    )
            else:
                mujoco_object_copy.mjcf_obj.worldbody.body[0].add("joint")
            self.mujoco_objects_rule_blueprints[name] = mujoco_object_copy

    def assemble_world(self) -> tuple[Environment, list[Area]]:
        """Assembles the world according to the users configuration.
        Returns:
            environment (Environment): Environment class instance
            areas (list[Area]): List of Area class instances
        """
        self.get_object_blueprints()
        size = self.config["Environment"]["size"]
        pretty_mode = self.config["Environment"]["Style"][0]["pretty_mode"]

        environment = Environment(
            name="Environment1", size=(size[0], size[1], 0.1), pretty_mode=pretty_mode
        )
        areas = [
            Area(
                name="Area1",
                size=(size[0], size[1], 0.1),
                environment=environment,
                boundary=None,
            )
        ]
        validators = self.create_validators(size, areas)

        self.place_border(environment, size, validators[0])
        self.place_fixed_objects(environment, areas, validators)
        self.place_random_objects(environment, areas, validators)
        self.add_base_plane(environment, size, pretty_mode)
        validators[0].plot(env_size=environment.size)

        return environment, areas

    def create_validators(self, size, areas):
        """Creates validators for environment and areas."""
        rules = [
            MinDistanceMujocoPhysicsRule(distance=1.0),
            BoundaryRule(boundary=(size[0], size[1])),
        ]
        environment_validator = Validator(rules)
        global_validators = [environment_validator]

        area_validators = [Validator(rules) for area in areas]

        return global_validators + area_validators

    def place_border(self, environment, size, validator):
        """Adds borders to the environment."""
        border_config_dict = {
            k: v
            for dict_ in self.config["Environment"]["Borders"]
            for k, v in dict_.items()
        }
        has_border = border_config_dict["place"]
        BorderPlacer().add(
            environment=environment,
            mujoco_object_blueprint=self.mujoco_objects_blueprints["Border"],
            amount=4,
            has_border=has_border,
        )

        if has_border:
            validator.map_2D[self.mujoco_objects_blueprints["Border"].name] = [
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

    def place_fixed_objects(self, environment, areas, validators):
        """Places objects with fixed coordinates at both environment and area level."""
        fixed_placer = FixedPlacer()
        sites_configs = [self.config["Environment"]["Objects"]] + [
            self.config["Areas"][area]["Objects"] for area in self.config["Areas"]
        ]
        for site_index, site in enumerate([environment] + areas):
            for object_name, object_settings in sites_configs[site_index].items():
                object_config_dict = {
                    k: v for dict_ in object_settings for k, v in dict_.items()
                }

                for objects in object_settings:
                    if "coordinates" in objects:
                        fixed_placer.add(
                            site=site,
                            mujoco_object_blueprint=self.mujoco_objects_blueprints[
                                object_name
                            ],
                            mujoco_object_rule_blueprint=self.mujoco_objects_rule_blueprints[
                                object_name
                            ],
                            validators=[validators[0], validators[site_index]],
                            amount=object_config_dict["amount"],
                            coordinates=objects["coordinates"],
                        )

    def place_random_objects(self, environment, areas, validators):
        """Places objects with random coordinates at both environment and area level."""
        environment_random_distribution = Placer2DDistribution(
            MultivariateUniform(),
            np.array(
                [
                    [-environment.size[0], environment.size[0]],
                    [-environment.size[1], environment.size[1]],
                ]
            ),
        )
        random_placer = RandomPlacer(distribution=environment_random_distribution)
        sites_configs = [self.config["Environment"]["Objects"]] + [
            self.config["Areas"][area]["Objects"] for area in self.config["Areas"]
        ]

        for site_index, site in enumerate([environment] + areas):
            for object_name, object_settings in sites_configs[site_index].items():
                if "coordinates" not in [
                    list(setting.keys())[0] for setting in object_settings
                ]:
                    object_config_dict = {
                        k: v for dict_ in object_settings for k, v in dict_.items()
                    }
                    colors_range = object_config_dict.get("colors", None)
                    sizes_range = object_config_dict.get("sizes", None)

                    random_placer.add(
                        site=site,
                        mujoco_object_blueprint=self.mujoco_objects_blueprints[
                            object_name
                        ],
                        mujoco_object_rule_blueprint=self.mujoco_objects_rule_blueprints[
                            object_name
                        ],
                        validators=[validators[0], validators[site_index]],
                        amount=object_config_dict["amount"],
                        colors_range=colors_range,
                        sizes_range=sizes_range,
                    )

    def add_base_plane(self, environment, size, pretty_mode):
        """Adds a base plane to the environment."""
        plane_options = {
            "name": "base_plane",
            "type": "plane",
            "size": (size[0], size[1], 0.1),
            "material": "grid" if pretty_mode else None,
        }

        environment.mjcf_model.worldbody.add(
            "geom", **{k: v for k, v in plane_options.items() if v is not None}
        )
