from shapely import geometry
import matplotlib.pyplot as plt

from pita_algorithm.base.asset_placement.abstract_rule import Rule
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class Validator:
    """Validates new objects against a set of rules and stores a 2d representation of the world."""

    def __init__(self, rules: list[Rule] = []):
        """Constructor of the Validator class.

        Parameters:
            rules (list[Rule]): List of Rules that have to be satisfied
        """
        self.map_2D = {}
        self.rules = rules

    def validate(self, mujoco_object: MujocoObject, site: AbstractSite) -> bool:
        """If all rules are satisfied, the new object will be included in the 2d representation
        and placement is valid.

        Parameters:
            mujoco_object (MujocoObject): the new object, that will be evaluated
            site (AbstractSite): AbstractSite class instance where the object is added to

        Returns:
            (bool): True if the new object satisfies all rules
        """
        shape_object = geometry.Point(mujoco_object.position[:2])

        for rule in self.rules:
            if not rule(
                map_2D=self.map_2D,
                shape_object=shape_object,
                mujoco_object=mujoco_object,
                site=site,
            ):
                return False

        return True

    def plot(self, env_size: list):
        """Plots the current 2d representation to where the current mpl backend points.

        Parameters:
            env_size (tuple[float, float, float]): Tuple containing the size of the environment
        """
        for index, shape_list in enumerate(self.map_2D.values()):
            # Directly plot the list of coordinates associated with each key in the Map2D dict
            try:
                x = [x.exterior.xy[0] for x in shape_list]
                y = [y.exterior.xy[1] for y in shape_list]

                plt.plot(x, y, label=list(self.map_2D.keys())[index])

            except AttributeError:
                x = [x.xy[0] for x in shape_list]
                y = [y.xy[1] for y in shape_list]

                plt.scatter(x, y, label=list(self.map_2D.keys())[index])

        # Custom plot configuration
        plt.xlim(-int(env_size[0]), int(env_size[0]))
        plt.xticks(range(-int(env_size[0]), int(env_size[0]) + 1))
        plt.locator_params(axis="x", nbins=10)
        plt.ylim(-int(env_size[1]), int(env_size[1]))
        plt.yticks(range(-int(env_size[1]), int(env_size[1]) + 1))
        plt.locator_params(axis="y", nbins=10)
        plt.legend()

        plt.show()

    def add(self, mujoco_object: MujocoObject):
        """Adds object to 2d representation.

        Parameters:
            mujoco_object (MujocoObject): The new object that will be added to the 2d representation
        """
        shape_object = geometry.Point(mujoco_object.position[:2])

        if mujoco_object.name in self.map_2D.keys():
            self.map_2D[mujoco_object.name].append(shape_object)

        else:
            self.map_2D[mujoco_object.name] = [shape_object]
