import re
from shapely.geometry.base import BaseGeometry

from pita_algorithm.base.asset_placement.abstract_rule import Rule
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from pita_algorithm.base.world_container.abstract_container import AbstractContainer


class MinDistanceRule(Rule):
    """Check if a new object respects the minimum distance to other objects, optionally of a specified type"""

    def __init__(self, dist: float, types: list([str, ...]) = []):
        """Initialize a new MinDistanceRule.

        Parameters:
            dist (float): Minimal distance from the new object to all existing of specified type
            types (list): By default all objects in the environment will be considered. Alternatively a list with names can be passed and all mjcf-objects that include any of these names are considered, only. Can be regex.
        """
        self.dist = dist
        self.types = types

    def __call__(
        self,
        map_2D: dict,
        shape_object: BaseGeometry,
        mujoco_object: MujocoObject,
        site: AbstractContainer,
    ):
        """Check if a new object satisfies the rule.

        Parameters:
            map_2D (dict): Dictionary, mapping object classes to a list of their shapely 2d representations
            shape_object (BaseGeometry): Insertion that should be evaluated
            mujoco_object (MujocoObject): The new object, that will be evaluated
            site (AbstractContainer): AbstractContainer class instance where the object is added to

        Returns:
            (boolean): True if shape_object is far enough away from each object. If self.types is not empty, only objects of the specified type are considered.
        """
        for obj_class in map_2D:
            # If a type is specified, only validate against it
            # TODO: currently does not work --> do we even need it?
            matches = [re.search(pattern, obj_class) for pattern in self.types]
            if any(matches) or not matches:
                # Iterate over all placed objects within the map_2D[obj_class] list
                for obj in map_2D[obj_class]:
                    if shape_object.distance(obj) < self.dist:
                        return False
        return True
