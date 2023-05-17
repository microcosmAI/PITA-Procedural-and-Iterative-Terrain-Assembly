import copy
import numpy as np
from dm_control import mjcf

from peters_algorithm.base.world_container.area import Area
from peters_algorithm.base.asset_placement.validator import Validator
from peters_algorithm.base.world_container.environment import Environment
from peters_algorithm.base.asset_parsing.mujoco_loader import MujocoLoader
from peters_algorithm.base.asset_placement.fixed_placer import FixedPlacer
from peters_algorithm.base.asset_placement.random_placer import (
    RandomPlacer,
    Placer2DDistribution,
)
from peters_algorithm.base.asset_placement.border_placer import BorderPlacer
from peters_algorithm.base.asset_placement.boundary_rule import BoundaryRule
from peters_algorithm.base.asset_placement.min_distance_rule import MinDistanceRule
from peters_algorithm.base.asset_placement.min_distance_mujoco_physics_rule import (
    MinDistanceMujocoPhysicsRule,
)


# from peters_algorithm.base.asset_placement.global_placer import GlobalPlacer


class Assembler:
    """Assembles assets to corresponding world container"""

    def __init__(self, config_file: dict, xml_dir: str):
        """Constructor for Assembler class

        Parameters:
            config (dict): config file containing user defined parameters
            xml_dir (str): string to xml-directory (containing assets)
        """
        self.config = config_file
        self.xml_dir = xml_dir

    def assemble_world(self) -> tuple[Environment, list[Area]]:
        """Calls the environment and areas and assembles them to create the world as and MJCF object

        Returns:
            environment (Environment): Environment class instance
            areas (list): List of Area class instances
        """
        # call mujoco loader to get dictionary of mujoco objects
        mujoco_loader = MujocoLoader(config_file=self.config, xml_dir=self.xml_dir)
        mujoco_objects_blueprints = mujoco_loader.get_mujoco_objects()

        # duplicate blueprints for rule checking that can be manipulated without changing the original
        mujoco_objects_rule_blueprints = {}
        for name, mujoco_object in mujoco_objects_blueprints.items():
            mujoco_object_copy = copy.deepcopy(mujoco_object)
            mujoco_object_copy.mjcf_obj.worldbody.body[0].add("joint")
            mujoco_objects_rule_blueprints[name] = mujoco_object_copy

        # parse size from the config
        size = self.config["Environment"]["size"]
        pretty_mode = self.config["Environment"]["Style"][0]["pretty_mode"]

        # create environment
        environment = Environment(
            name="Environment1", size=(size[0], size[1], 0.1), pretty_mode=pretty_mode
        )

        # create areas
        # as long as we only have one area we set its size to the one of the env
        # TODO: set size with layout manager
        areas = [Area(name="area1", size=(size[0], size[1], 0.1))]
        """for area_name, area_settings in self.config["Areas"].items():
            areas.append(Area(name=area_name, size=(10, 10, 0.1)))"""

        # Create Validators
        environment_validator = Validator(
            [
                MinDistanceMujocoPhysicsRule(2.0),
                BoundaryRule(boundary=(size[0], size[1])),
            ]
        )

        global_validators = [
            environment_validator,
        ]

        area_validators = []
        for area_index, (area_name, area_settings) in enumerate(
            self.config["Areas"].items()
        ):
            area_validators.append(
                Validator(
                    [
                        MinDistanceMujocoPhysicsRule(2.0),
                        BoundaryRule(boundary=(size[0], size[1])),
                    ]
                )
            )

        # Border Placement
        # TODO: if config.environment.borders:
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

        # TODO: Maybe see if its possible to not loop over these item a second time for random placement
        # Fixed Coordinate Mujoco Object Placement - Environment level
        for object_name, object_settings in self.config["Environment"][
            "Objects"
        ].items():
            object_config_dict = {}
            for dict_ in object_settings:
                object_config_dict.update(dict_)

            for objects in object_settings:
                if "coordinates" in objects:
                    FixedPlacer().add(
                        site=environment,
                        mujoco_object_blueprint=mujoco_objects_blueprints[object_name],
                        mujoco_objects_rule_blueprint=mujoco_objects_rule_blueprints[
                            object_name
                        ],
                        validators=global_validators,
                        amount=object_config_dict["amount"],
                        coordinates=objects["coordinates"],
                    )

        # Fixed Coordinate Mujoco Object Placement - Area level
        for area_index, (area_name, area_settings) in enumerate(
            self.config["Areas"].items()
        ):
            for object_name, object_settings in area_settings["Objects"].items():
                object_config_dict = {}
                for dict_ in object_settings:
                    object_config_dict.update(dict_)

                for objects in object_settings:
                    if "coordinates" in objects:
                        FixedPlacer().add(
                            site=areas[area_index],
                            mujoco_object_blueprint=mujoco_objects_blueprints[
                                object_name
                            ],
                            mujoco_objects_rule_blueprints=mujoco_objects_rule_blueprints[
                                object_name
                            ],
                            validators=[
                                area_validators[area_index],
                            ]
                            + global_validators,
                            amount=object_config_dict["amount"],
                            coordinates=objects["coordinates"],
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

                # checks for color and size range which the random placer with handle
                if "colors" not in [
                    list(setting.keys())[0] for setting in object_settings
                ]:
                    colors_range = None
                else:
                    colors_range = object_config_dict["colors"]
                if "sizes" not in [
                    list(setting.keys())[0] for setting in object_settings
                ]:
                    sizes_range = None
                else:
                    sizes_range = object_config_dict["sizes"]

                environment_random_distribution = Placer2DDistribution(
                    np.random.multivariate_normal,
                    (0, 0),
                    np.array([[environment.size[0], 0], [0, environment.size[1]]]),
                )
                RandomPlacer(environment_random_distribution).add(
                    site=environment,
                    mujoco_object_blueprint=mujoco_objects_blueprints[object_name],
                    mujoco_objects_rule_blueprint=mujoco_objects_rule_blueprints[
                        object_name
                    ],
                    validators=global_validators,
                    amount=object_config_dict["amount"],
                    colors_range=colors_range,
                    sizes_range=sizes_range,
                )

        # Random Mujoco Object Placement - Area level
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

                    # checks for color and size range which the random placer with handle
                    if "colors" not in [
                        list(setting.keys())[0] for setting in object_settings
                    ]:
                        colors_range = None
                    else:
                        colors_range = object_config_dict["colors"]
                    if "sizes" not in [
                        list(setting.keys())[0] for setting in object_settings
                    ]:
                        sizes_range = None
                    else:
                        sizes_range = object_config_dict["sizes"]

                    area_random_distribution = Placer2DDistribution(
                        np.random.multivariate_normal,
                        (0, 0),
                        np.array(
                            [
                                [areas[area_index].size[0], 0],
                                [0, areas[area_index].size[1]],
                            ]
                        ),
                    )
                    RandomPlacer(area_random_distribution).add(
                        site=areas[area_index],
                        mujoco_object_blueprint=mujoco_objects_blueprints[object_name],
                        mujoco_objects_rule_blueprint=mujoco_objects_rule_blueprints[
                            object_name
                        ],
                        validators=[
                            area_validators[area_index],
                        ]
                        + global_validators,
                        amount=object_config_dict["amount"],
                        colors_range=colors_range,
                        sizes_range=sizes_range,
                    )

        # Use global validator to plot the map layout
        global_validators[0].plot(env_size=environment.size)

        # Add plane
        if pretty_mode:
            environment.mjcf_model.worldbody.add(
                "geom",
                name="base_plane",
                type="plane",
                size="10 10 0.10000000000000001",
                material="grid",
            )
        else:
            environment.mjcf_model.worldbody.add(
                "geom",
                name="base_plane",
                type="plane",
                size="10 10 0.10000000000000001",
            )

        for area in areas:
            environment.mjcf_model.attach(area.mjcf_model)

        return environment, areas
