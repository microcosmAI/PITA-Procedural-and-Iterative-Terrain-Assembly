import re
from shapely import geometry
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from shapely.geometry.base import BaseGeometry

from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class Rule(ABC):
    """Abstract class for rules."""

    @abstractmethod
    def __call__(self, map2d: dict, shape: BaseGeometry):
        pass


class MinDistanceRule(Rule):
    """Check if a new object respects the minimum distance to other objects of a specified type"""

    def __init__(self, dist: float, types: list([str, ...]) = []):
        """Initialize a new MinDistanceRule.

        Parameters:
            dist (float): Minimal distance from the new object to all existing of specified type
            types (list): By default all objects in the environment will be considered. Alternatively a list with names can be passed and all mjcf-objects that include any of these names are considered, only. Can be regex.
        """
        self.dist = dist
        self.types = types

    def __call__(self, map_2D: dict, shape_object: BaseGeometry):
        """Check if a new object satisfies the rule.

        Parameters:
            map_2D (dict): Dictionary, mapping names of objects to their shapely 2d representation
            shape (BaseGeometry): Insertion that should be evaluated

        Returns:
            True if shape is far enough away from each object that has any of self.types in their name.
        """
        for obj in map_2D:
            matches = [re.search(pattern, obj) for pattern in self.types]
            if any(matches) or not matches:
                if shape_object.distance(map_2D[obj]) < self.dist:
                    return False
        return True


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
