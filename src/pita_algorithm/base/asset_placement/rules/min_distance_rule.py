import re
from shapely.geometry.base import BaseGeometry
from pita_algorithm.base.asset_placement.rules.abstract_rule import Rule
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class MinDistanceRule(Rule):
    """Check if a new object respects the minimum distance to other objects."""

    def __init__(self, dist: float, types: list[str] = []):
        """Constructor of the MinDistanceRule class.

        Parameters:
            dist (float): Minimal distance from the new object to all existing of specified type
            types (list): By default all objects in the environment will be considered.
        """
        super().__init__()
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
            (bool): True if shape_object is far enough away from each object
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
