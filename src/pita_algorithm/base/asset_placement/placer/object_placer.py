import logging
from shapely import geometry
from pita_algorithm.utils.general_utils import Utils
from pita_algorithm.base.world_sites.area import Area
from pita_algorithm.base.world_sites.environment import Environment
from pita_algorithm.base.asset_placement.validator import Validator
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_placement.placer.fixed_placer import FixedPlacer
from pita_algorithm.base.asset_placement.placer.random_placer import RandomPlacer
from pita_algorithm.base.asset_placement.placer.border_placer import BorderPlacer


class ObjectPlacer:
    """Places objects in the world (environment and areas)."""

    def __init__(self, config: dict, blueprints: dict):
        """Constructor of the ObjectPlacer class.

        Parameters:
            config (dict): Configuration dictionary
            blueprints (dict): Dictionary of Mujoco objects blueprints
            rule_blueprints (dict): Dictionary of Mujoco objects rule blueprints

        """
        self.config = config
        self.blueprints = blueprints

    def place_objects(
        self, environment: Environment, areas: list[Area], validators: list[Validator]
    ) -> None:
        """Places all types of objects (border, fixed, random) in the world.

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
        logger = logging.getLogger()
        border_config_dict = {
            k: v
            for dict_ in self.config["Environment"]["Borders"]
            for k, v in dict_.items()
        }
        has_border = border_config_dict["place"]
        logger.info("Placing borders..")
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
        """Places fixed or random objects in the world sites.

        Parameters:
            sites (list[AbstractSite]): List of Site objects
            validators (list[Validator]): List of Validator objects
            is_fixed (bool): True if the objects should be placed with fixed coordinates, False otherwise
        """
        sites_configs = self._get_site_configs(sites)
        for site_index, site in enumerate(sites):
            logging.info(f"Entering site '{sites[site_index].name}'..")
            for object_name, object_settings in sites_configs[site_index].items():
                logging.info(
                    f"Trying to place object(s) '{object_name}' in '{sites[site_index].name}'"
                )
                placer: FixedPlacer | RandomPlacer = (
                    FixedPlacer() if is_fixed else RandomPlacer()
                )
                if self._should_place_object(is_fixed, object_settings):
                    object_config_dict = {
                        k: v for dict_ in object_settings for k, v in dict_.items()
                    }
                    placer.add(
                        site=site,
                        mujoco_object_blueprint=self.blueprints[object_name],
                        validators=[validators[0], validators[site_index]],
                        amount=object_config_dict["amount"],
                        mujoco_objects_blueprints=self.blueprints,
                        **self._get_placer_params(object_config_dict, is_fixed),
                    )

    def _get_site_configs(self, sites: list[AbstractSite]) -> list[dict]:
        """Returns the object configurations for all world sites.

        Parameters:
            sites (list[AbstractSite]): List of Site objects

        Returns:
            list (dict): List of configuration dictionaries depending on site type
        """
        return [
            self.config["Environment"]["Objects"]
            if "Environment" in site.name
            else self.config["Areas"][site.name]["Objects"]
            for site in sites
        ]

    @staticmethod
    def _should_place_object(is_fixed: bool, object_settings: list[dict]) -> bool:
        """Returns whether an object should be placed based on the given settings.

        Parameters:
            is_fixed (bool): True if the objects should be placed with fixed coordinates, False otherwise
            object_settings (list[dict]): List of dictionaries containing the object settings

        Returns:
            bool: True if the object is fixed, False otherwise
        """
        has_coordinates = "coordinates" in [
            list(setting.keys())[0] for setting in object_settings
        ]
        return has_coordinates if is_fixed else not has_coordinates

    @staticmethod
    def _get_placer_params(config_dict: dict, is_fixed: bool) -> dict:
        """Returns the specific parameters needed for the placer, based on the given settings.

        Parameters:
            config_dict (dict): Dictionary containing the object settings
            is_fixed (bool): True if the objects should be placed with fixed coordinates, False otherwise

        Returns:
            combined_dict (dict): Dictionary containing additional optional parameters
        """
        keys = [
            "z_rotation_range",
            "color_groups",
            "size_groups",
            "size_value_range",
            "asset_pool",
        ]

        values = Utils.get_randomization_parameters(config_dict=config_dict, keys=keys)
        combined_dict = {k: v for k, v in zip(keys, values)}

        if is_fixed:
            combined_dict["coordinates"] = (
                config_dict["coordinates"] if "coordinates" in config_dict else None
            )
        else:
            combined_dict["distribution"] = (
                config_dict["distribution"] if "distribution" in config_dict else None
            )
        return combined_dict
