import copy

from shapely import geometry

from pita_algorithm.base.asset_parsing.mujoco_loader import MujocoLoader
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from pita_algorithm.base.asset_placement.border_placer import BorderPlacer
from pita_algorithm.base.asset_placement.boundary_rule import BoundaryRule

from pita_algorithm.base.asset_placement.fixed_placer import FixedPlacer
from pita_algorithm.base.asset_placement.min_distance_mujoco_physics_rule import (
    MinDistanceMujocoPhysicsRule,
)
from pita_algorithm.base.asset_placement.multivariate_uniform_distribution import (
    MultivariateUniformDistribution,

)
from pita_algorithm.base.asset_placement.random_placer import (
    RandomPlacer,
)

from pita_algorithm.base.asset_placement.validator import Validator
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.world_sites.area import Area
from pita_algorithm.base.world_sites.environment import Environment
from pita_algorithm.utils.general_utils import Utils



class BlueprintManager:
    """Creates and manages the Mujoco objects blueprints"""

    def __init__(self, config: dict, xml_dir: str) -> None:
        """Constructor of the BlueprintManager class.

        Parameters:
            config (dict): Configuration dictionary
            xml_dir (str): Path to the xml files
        """
        self.config: dict = config
        self.xml_dir: str = xml_dir
        self.mujoco_objects_blueprints: dict[str, MujocoObject] = {}
        self.mujoco_objects_rule_blueprints: dict[str, MujocoObject] = {}

    def get_object_blueprints(self) -> None:
        """Creates and manipulates the mujoco objects blueprints."""
        mujoco_loader = MujocoLoader(config_file=self.config, xml_dir=self.xml_dir)
        self.mujoco_objects_blueprints = mujoco_loader.get_mujoco_objects()

        for name, mujoco_object in self.mujoco_objects_blueprints.items():
            mujoco_object_copy = self._create_rule_blueprint(mujoco_object)
            self.mujoco_objects_rule_blueprints[name] = mujoco_object_copy

    @staticmethod
    def _create_rule_blueprint(mujoco_object: MujocoObject) -> MujocoObject:
        """Creates rule blueprints for Mujoco objects.

        Parameters:
            mujoco_object (MujocoObject): Mujoco object to be manipulated
        """
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
        return mujoco_object_copy


class ObjectPlacer:
    """Places objects in the environment."""

    def __init__(self, config: dict, blueprints: dict, rule_blueprints: dict) -> None:
        """Constructor of the ObjectPlacer class.

        Parameters:
            config (dict): Configuration dictionary
            blueprints (dict): Dictionary of Mujoco objects blueprints
            rule_blueprints (dict): Dictionary of Mujoco objects rule blueprints

        """
        self.config = config
        self.blueprints = blueprints
        self.rule_blueprints = rule_blueprints

    def place_objects(
        self, environment: Environment, areas: list[Area], validators: list[Validator]
    ) -> None:
        """Places all types of objects (border, fixed, random) in the environment.

        Parameters:
            environment (Environment): Environment object
            areas (list[Area]): List of Area objects
            validators (list[Validator]): List of Validator objects

        """
        self._place_border(environment, validators[0])
        # Global placer
        self._place_objects_in_sites(
            [
                environment,
            ],
            validators,
            is_fixed=True,
        )
        if self.config.get("Areas") is not None:
            self._place_objects_in_sites(areas, validators, is_fixed=True)
        self._place_objects_in_sites(
            [
                environment,
            ],
            validators,
            is_fixed=False,
        )
        if self.config.get("Areas") is not None:
            self._place_objects_in_sites(areas, validators, is_fixed=False)

    def _place_border(self, environment: Environment, validator: Validator) -> None:
        """Places borders in the environment.

        Parameters:
            environment (Environment): Environment object
            validator (Validator): Validator object
        """
        border_config_dict = {
            k: v
            for dict_ in self.config["Environment"]["Borders"]
            for k, v in dict_.items()
        }
        has_border = border_config_dict["place"]
        BorderPlacer().add(
            environment=environment,
            mujoco_object_blueprint=self.blueprints["Border"],
            amount=4,
            has_border=has_border,
        )

        if has_border:
            validator.map_2D[self.blueprints["Border"].name] = [
                geometry.LineString(
                    [
                        [-environment.size[0], -environment.size[1]],
                        [-environment.size[0], environment.size[1]],
                        [environment.size[0], environment.size[1]],
                        [environment.size[0], -environment.size[1]],
                        [-environment.size[0], -environment.size[1]],
                    ]
                )
            ]


    def _place_objects_in_sites(
        self, sites: list[AbstractSite], validators: list[Validator], is_fixed: bool
    ) -> None:
        """Places fixed or random objects in the environment.

        Parameters:
            sites (list[AbstractSite]): List of Site objects
            validators (list[Validator]): List of Validator objects
            is_fixed (bool): True if the objects should be placed with fixed coordinates, False otherwise
        """
        sites_configs = self._get_site_configs(sites)
        for site_index, site in enumerate(sites):
            for object_name, object_settings in sites_configs[site_index].items():
                placer: FixedPlacer | RandomPlacer = (
                    FixedPlacer() if is_fixed else self._get_random_placer(site)
                )
                if self._should_place_object(is_fixed, object_settings):
                    object_config_dict = {
                        k: v for dict_ in object_settings for k, v in dict_.items()
                    }
                    placer.add(
                        site=site,
                        mujoco_object_blueprint=self.blueprints[object_name],
                        mujoco_object_rule_blueprint=self.rule_blueprints[object_name],
                        validators=[validators[0], validators[site_index]],
                        amount=object_config_dict["amount"],
                        **self._get_placer_params(object_config_dict, is_fixed),
                    )

    def _place_objects_in_environment(
        self, environment: Environment, validators: list[Validator], is_fixed: bool
    ) -> None:
        """Places fixed or random objects in the environment.
        TODO: DEPRECATED
        Parameters:
            environment (Environment): Environment object
            validators (list[Validator]): List of Validator objects
            is_fixed (bool): True if the objects should be placed with fixed coordinates, False otherwise
        """
        placer: FixedPlacer | RandomPlacer = (
            FixedPlacer() if is_fixed else self._get_random_placer(environment)
        )

        for object_name, object_settings in self.config["Environment"][
            "Objects"
        ].items():
            if self._should_place_object(is_fixed, object_settings):
                object_config_dict = {
                    k: v for dict_ in object_settings for k, v in dict_.items()
                }
                placer.add(
                    site=environment,
                    mujoco_object_blueprint=self.blueprints[object_name],
                    mujoco_object_rule_blueprint=self.rule_blueprints[object_name],
                    validators=[validators[0]],
                    amount=object_config_dict["amount"],
                    **self._get_placer_params(object_config_dict, is_fixed),
                )

    def _place_objects_in_areas(
        self, areas: list[Area], validators: list[Validator], is_fixed: bool
    ) -> None:
        """Places fixed or random objects in the areas.
        TODO: DEPRECATED
        Parameters:
            areas (list[Area]): List of Area objects
            validators (list[Validator]): List of Validator objects
            is_fixed (bool): True if the objects should be placed with fixed coordinates, False otherwise
        """
        for area_index, area in enumerate(areas):
            for object_name, object_settings in self.config["Areas"][area.name][
                "Objects"
            ].items():
                if self._should_place_object(is_fixed, object_settings):
                    object_config_dict = {
                        k: v for dict_ in object_settings for k, v in dict_.items()
                    }
                    placer: FixedPlacer | RandomPlacer = (
                        FixedPlacer() if is_fixed else self._get_random_placer(area)
                    )
                    placer.add(
                        site=area,
                        mujoco_object_blueprint=self.blueprints[object_name],
                        mujoco_object_rule_blueprint=self.rule_blueprints[object_name],
                        validators=[validators[0], validators[area_index]],
                        amount=object_config_dict["amount"],
                        **self._get_placer_params(object_config_dict, is_fixed),
                    )

    def _get_site_configs(self, sites: list[AbstractSite]) -> list[dict]:
        """Returns the object configurations for all sites.

        Parameters:
            sites (list[AbstractSite]): List of Site objects

        """
        return [
            self.config["Environment"]["Objects"]
            if "Environment" in site.name
            else self.config["Areas"][site.name]["Objects"]
            for site in sites
        ]

    @staticmethod
    def _get_random_placer(site: AbstractSite) -> RandomPlacer:
        """Creates and returns a RandomPlacer instance.

        Parameters:
            site (AbstractSite): AbstractSite object
        """
        distribution = MultivariateUniformDistribution(
            parameters={
                "low": [-site.size[0], -site.size[1]],
                "high": [site.size[0], site.size[1]],
            }
        )
        return RandomPlacer(distribution=distribution)

    @staticmethod
    def _should_place_object(is_fixed: bool, object_settings: list[dict]) -> bool:
        """Returns whether an object should be placed based on the given settings.

        Parameters:
            is_fixed (bool): True if the objects should be placed with fixed coordinates, False otherwise
            object_settings (list[dict]): List of dictionaries containing the object settings
        """
        has_coordinates = "coordinates" in [
            list(setting.keys())[0] for setting in object_settings
        ]
        return has_coordinates if is_fixed else not has_coordinates

    def _get_placer_params(self, config_dict: dict, is_fixed: bool) -> dict:
        """Returns the specific parameters needed for the placer, based on the given settings.

        Parameters:
            config_dict (dict): Dictionary containing the object settings
            is_fixed (bool): True if the objects should be placed with fixed coordinates, False otherwise
        """
        if is_fixed:
            return {
                "coordinates": config_dict["coordinates"]
                if "coordinates" in config_dict
                else None
            }
        else:
            keys = [
                "z_rotation_range",
                "color_groups",
                "size_groups",
                "size_value_range",
            ]

            values = Utils._get_randomization_parameters(
                config_dict=config_dict, keys=keys
            )
            combined_dict = {k: v for k, v in zip(keys, values)}
            return combined_dict


class Assembler:
    """Assembles the environment."""

    def __init__(self, config_file: dict, xml_dir: str) -> None:
        """Constructor of the Assembler class.

        Parameters:
            config_file (dict): Dictionary containing the configuration
            xml_dir (str): Path to the directory containing the xml files

        """
        self.config = config_file
        self.xml_dir = xml_dir

    def assemble_world(self) -> tuple[Environment, list[Area]]:
        """Assembles the world according to the users configuration and returns the environment and areas."""
        blueprint_manager = BlueprintManager(self.config, self.xml_dir)
        blueprint_manager.get_object_blueprints()

        environment, areas = self._create_environment_and_areas()
        validators = self._create_validators(environment.size, areas)

        object_placer = ObjectPlacer(
            self.config,
            blueprint_manager.mujoco_objects_blueprints,
            blueprint_manager.mujoco_objects_rule_blueprints,
        )
        object_placer.place_objects(environment, areas, validators)

        self._add_base_plane(environment)
        validators[0].plot(env_size=environment.size)

        return environment, areas

    def _create_environment_and_areas(self) -> tuple[Environment, list[Area]]:
        """Creates and returns the environment and areas."""
        size_range = Utils._get_randomization_parameters(
            config_dict=self.config["Environment"], keys=["size_range"]
        )
        pretty_mode = self.config["Environment"]["Style"][0]["pretty_mode"]

        environment = Environment(
            name="Environment1", size=size_range, pretty_mode=pretty_mode
        )

        areas = []
        if self.config.get("Areas") is not None:
            for area_index, area_config in enumerate(self.config["Areas"].items()):
                areas.append(
                    Area(
                        name=f"Area{area_index + 1}",
                        size=(
                            environment.size[0],
                            environment.size[1],
                            0.1,
                        ),  # TODO Get Size from Area Config or Layoutmanager ?!?!
                        environment=environment,
                        boundary=None,
                    )
                )
        return environment, areas

    @staticmethod
    def _create_validators(
        size: tuple[float, float, float], areas: list[Area]
    ) -> list[Validator]:
        """Creates and returns the validators for the environment and areas.

        Parameters:
            size (tuple[float, float]): Size of the environment
            areas (list[Area]): List of Area objects
        """
        rules = [
            MinDistanceMujocoPhysicsRule(distance=1.0),
            BoundaryRule(boundary=(size[0], size[1])),
        ]
        environment_validator = Validator(rules)
        area_validators = [Validator(rules) for area in areas]
        return [environment_validator] + area_validators

    def _add_base_plane(self, environment: Environment) -> None:
        """Adds a base plane to the environment.

        Parameters:
            environment (Environment): Environment object
        """
        pretty_mode = self.config["Environment"]["Style"][0]["pretty_mode"]
        plane_options = {
            "name": "base_plane",
            "type": "plane",
            "size": (environment.size[0], environment.size[1], 0.1),
            "material": "grid" if pretty_mode else None,
        }
        environment.mjcf_model.worldbody.add(
            "geom", **{k: v for k, v in plane_options.items() if v is not None}
        )
