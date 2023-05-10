from dm_control import mjcf

from peters_algorithm.base.world_container.area import Area
from peters_algorithm.base.world_container.environment import Environment
from peters_algorithm.base.asset_parsing.mujoco_loader import MujocoLoader
from peters_algorithm.base.asset_placement.fixed_placer import FixedPlacer
from peters_algorithm.base.asset_placement.random_placer import RandomPlacer
from peters_algorithm.base.asset_placement.border_placer import BorderPlacer


# from peters_algorithm.base.asset_placement.global_placer import GlobalPlacer
from peters_algorithm.base.asset_placement.validator import Validator
from peters_algorithm.base.asset_placement.min_distance_rule import MinDistanceRule


class Assembler:
    """Assembles assets to corresponding world container

    Attributes
    ----------
        config (dict): config file containing user defined parameters
        xml_dir (str): string to xml-directory (containing assets)
    """

    def __init__(self, config_file: dict, xml_dir: str):
        self.config = config_file
        self.xml_dir = xml_dir

    def assemble_world(self) -> mjcf:
        """Calls the environment and areas and assembles them to create the world as and MJCF object"""
        # call mujoco loader to get dictionary of mujoco objects
        mujoco_loader = MujocoLoader(config_file=self.config, xml_dir=self.xml_dir)
        mujoco_objects_blueprints = mujoco_loader.get_mujoco_objects()

        # create environment
        environment = Environment(name="Environment1", size=(10, 10, 0.1))

        # create areas
        areas = [Area(name="area1", size=(10, 10, 0.1))]
        """for area_name, area_settings in self.config["Areas"].items():
            areas.append(Area(name=area_name, size=(10, 10, 0.1)))"""

        # Create Validators
        minDistanceValidator = Validator(
            [
                MinDistanceRule(1.0),
            ]
        )
        validators = [
            minDistanceValidator,
        ]

        # Border Placement
        # TODO: if config.environment.borders:
        has_border = self.config["Environment"]["Borders"][0]["place"]
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
            for objects in object_settings:
                if "coordinates" in objects:
                    FixedPlacer().add(
                        site=environment,
                        mujoco_object_blueprint=mujoco_objects_blueprints[object_name],
                        validators=validators,
                        amount=object_settings[0]["amount"],
                        coordinates=objects["coordinates"],
                    )

        # Fixed Coordinate Mujoco Object Placement - Area level
        for area_index, (area_name, area_settings) in enumerate(
            self.config["Areas"].items()
        ):
            for object_name, object_settings in area_settings["Objects"].items():
                for objects in object_settings:
                    if "coordinates" in objects:
                        FixedPlacer().add(
                            site=areas[area_index],
                            mujoco_object_blueprint=mujoco_objects_blueprints[
                                object_name
                            ],
                            validators=validators,
                            amount=object_settings[0]["amount"],
                            coordinates=objects["coordinates"],
                        )

        # Random Mujoco Object Placement - Environment level
        for object_name, object_settings in self.config["Environment"][
            "Objects"
        ].items():
            if "coordinates" not in [
                list(setting.keys())[0] for setting in object_settings
            ]:
                RandomPlacer().add(
                    site=environment,
                    mujoco_object_blueprint=mujoco_objects_blueprints[object_name],
                    validators=validators,
                    amount=object_settings[0]["amount"],
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
                    # checks for color and size range which the random placer with handle
                    if "colors" not in [list(setting.keys())[0] for setting in object_settings]:
                        colors_range = None
                    else:
                        colors_range = object_settings[2]["colors"]
                    if "sizes" not in [list(setting.keys())[0] for setting in object_settings]:
                        sizes_range = None
                    else:
                        sizes_range = object_settings[3]["sizes"]

                    RandomPlacer().add(
                        site=areas[area_index],
                        mujoco_object_blueprint=mujoco_objects_blueprints[object_name],
                        validators=validators,
                        amount=object_settings[0]["amount"],
                        colors_range=colors_range,
                        sizes_range=sizes_range
                    )

        # Use global validator to plot the map layout
        validators[0].plot(env_size=environment.size)

        for area in areas:
            environment.mjcf_model.attach(area.mjcf_model)

        return environment
