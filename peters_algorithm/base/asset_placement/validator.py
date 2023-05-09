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
        # TODO: maybe inclue global coordinates of env
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

        self.map_2D.update({mujoco_object.name: shape_object})
        return True

    def plot(self):
        """Plot the current 2d representation to where ever the current mpl backend points."""
        for shape in self.map_2D.values():
            try:
                plt.plot(*shape.exterior.xy)
            except AttributeError:
                plt.scatter(*shape.xy)
        plt.show()
