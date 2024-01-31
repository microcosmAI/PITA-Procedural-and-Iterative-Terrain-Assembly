import logging
from pita_algorithm.utils.general_utils import Utils
from pita_algorithm.base.world_sites.area import Area
from pita_algorithm.base.world_sites.environment import Environment
from pita_algorithm.base.asset_placement.validator import Validator
from pita_algorithm.base.asset_placement.layout_manager import LayoutManager
from pita_algorithm.base.asset_placement.rules.boundary_rule import BoundaryRule
from pita_algorithm.base.asset_parsing.blueprint_manager import BlueprintManager
from pita_algorithm.base.asset_placement.placer.object_placer import ObjectPlacer
from pita_algorithm.base.asset_placement.rules.min_distance_mujoco_physics_rule import (
    MinDistanceMujocoPhysicsRule,
)


class Assembler:
    """Assembles the world."""

    def __init__(self, config_file: dict, xml_dir: str, plot: bool = False) -> None:
        """Constructor of the Assembler class.

        Parameters:
            config_file (dict): Dictionary containing the configuration
            xml_dir (str): Path to the directory containing the xml files
            plot (bool): Set to True for plotting
        """
        self.config = config_file
        self.xml_dir = xml_dir
        self.plot = plot

    def assemble_world(self) -> tuple[Environment, list[Area]]:
        """Assembles the world according to the users configuration and returns the environment and areas."""
        logger = logging.getLogger()

        logger.info("Loading assets..")
        blueprint_manager = BlueprintManager(self.config, self.xml_dir)
        blueprint_manager.get_object_blueprints()

        logger.info("Creating environment..")
        environment, areas = self._create_environment_and_areas(plot=self.plot)
        validators = self._create_validators(environment.size, areas)

        logger.info("Placing objects..")
        object_placer = ObjectPlacer(
            self.config,
            blueprint_manager.mujoco_objects_blueprints,
            blueprint_manager.mujoco_objects_rule_blueprints,
        )
        object_placer.place_objects(environment, areas, validators)

        self._add_base_plane(environment)
        if self.plot:
            validators[0].plot(env_size=environment.size)

        return environment, areas

    def _create_environment_and_areas(
        self, plot: bool
    ) -> tuple[Environment, list[Area]]:
        """Creates and returns the environment and areas."""
        size_range = Utils.get_randomization_parameters(
            config_dict=self.config["Environment"], keys=["size_range"]
        )
        pretty_mode = self.config["Environment"]["Style"][0]["pretty_mode"]

        environment = Environment(
            name="Environment1", size=size_range, pretty_mode=pretty_mode
        )

        areas = []
        if self.config.get("Areas") is not None:
            # Create boundaries with Layoutmanager
            areas_count = len(self.config["Areas"].items())
            layoutmanager = LayoutManager(
                environment.size[0] * 2, environment.size[1] * 2, areas_count, plot=plot
            )
            boundaries = layoutmanager.generate_layout_boundaries()
            layoutmanager.plot_boundaries(boundaries)

            # Convert from zero based coordinates to mujoco coordinates
            # So the 0,0 point is in the middle of the environment
            # Create a new list to store the modified boundaries
            modified_boundaries = []

            # Iterate through the original boundaries and perform modifications
            for boundary in boundaries:
                new_boundary_start = (
                    boundary[0][0] - environment.size[0],
                    boundary[0][1] - environment.size[1],
                )
                new_boundary_end = (
                    boundary[1][0] - environment.size[0],
                    boundary[1][1] - environment.size[1],
                )
                modified_boundary = (new_boundary_start, new_boundary_end)
                modified_boundaries.append(modified_boundary)
            boundaries = modified_boundaries

            # Create Areas
            for area_index, area_config in enumerate(self.config["Areas"].items()):
                areas.append(
                    Area(
                        name=f"Area{area_index + 1}",
                        size=(
                            (
                                boundaries[area_index][1][0]
                                - boundaries[area_index][0][0]
                            )
                            / 2,
                            (
                                boundaries[area_index][1][1]
                                - boundaries[area_index][0][1]
                            )
                            / 2,
                            0.1,
                        ),
                        environment=environment,
                        boundary=boundaries[area_index],
                    )
                )
        return environment, areas

    @staticmethod
    def _create_validators(size: list, areas: list[Area]) -> list[Validator]:
        """Creates and returns the validators for the environment and areas.

        Parameters:
            size (list): Size of the environment
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
