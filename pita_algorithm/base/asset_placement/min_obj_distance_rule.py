from shapely.geometry.base import BaseGeometry

from pita_algorithm.base.asset_placement.abstract_rule import Rule
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class MinObjDistanceRule(Rule):
    """Check if a new object respects the minimum distance to other objects of specified types."""

    def __init__(self, dist: float, types: list[str] = []):
        """Constructor of the MinObjDistanceRule class.

        Parameters:
            dist (float): Minimal distance from the new object to all existing of specified type
            types (list): Types of objects to consider
        """
        self.dist = dist
        self.types = types

    def __call__(
        self,
        map_2D: dict,
        shape_object: BaseGeometry,
        mujoco_object: MujocoObject,
        site: AbstractSite,
    ) -> bool:
        """Check if a new object satisfies the rule. Only utilizes map_2D and shape_object.

        Parameters:
            map_2D (dict): Dict mapping object classes to a list of their shapely representations
            shape_object (BaseGeometry): Insertion that should be evaluated
            mujoco_object (MujocoObject): The new object, that will be evaluated
            site (AbstractSite): AbstractSite class instance where the object is added to

        Returns:
            (bool): True if shape_object is far enough away from each object of specified types
        """
        for obj_class in map_2D:
            if obj_class in self.types:
                for obj in map_2D[obj_class]:
                    if shape_object.distance(obj) < self.dist:
                        return False

        return True
