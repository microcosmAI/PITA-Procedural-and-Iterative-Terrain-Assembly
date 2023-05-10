from shapely import geometry
import matplotlib.pyplot as plt

from peters_algorithm.base.asset_placement.abstract_rule import Rule
from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class Validator:
    """Class for maintaining a 2D representation for validation purposes, could be static"""

    def __init__(self, rules: list([Rule, ...]) = []):
        """Initialize new Validator.

        Parameters:
            rules (list): List of Rule objects. Each time that a new object is validated, all Rules have to be satisfied in order for the validation to return True
        """
        # dict[str, list[geometry.Point]]
        self.map_2D = (
            {}
        )  # {str: BaseGeometry, ...} with str being the uniquely identifying mjcf name
        self.rules = rules

    def validate(self, mujoco_object: MujocoObject):
        """
        If all rules are satisfied, the new object will be included in the 2d representation and True is returned

        Parameters:
            mujoco_object (MujocoObject): the new object, that will be evaluated

        Returns:
            True if the new object satirsfies all rules
        """
        # TODO: not sure if the mjcf structure will be consistent all the time...
        shape_object = geometry.Point(mujoco_object.position[:2])
        for rule in self.rules:
            if not rule(self.map_2D, shape_object):
                return False

        return True

    def plot(self, env_size: tuple[int, int, float]):
        """Plot the current 2d representation to where ever the current mpl backend points.

        Parameters:
            env_size (tuple): Tuple containing the size of the environment
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
        plt.xlim(-env_size[0], env_size[0])
        plt.xticks(range(-env_size[0], env_size[0] + 1))
        plt.locator_params(axis="x", nbins=10)
        plt.ylim(-env_size[1], env_size[1])
        plt.yticks(range(-env_size[1], env_size[1] + 1))
        plt.locator_params(axis="y", nbins=10)
        plt.legend()
        plt.show()

    def add(self, mujoco_object: MujocoObject):
        """Add object to 2d representation

        Parameters:
            mujoco_object (MujocoObject): The new object, that will be added to the 2d representation
        """
        shape_object = geometry.Point(mujoco_object.position[:2])
        if mujoco_object.name in self.map_2D.keys():
            self.map_2D[mujoco_object.name].append(shape_object)
        else:
            self.map_2D[mujoco_object.name] = [shape_object]
