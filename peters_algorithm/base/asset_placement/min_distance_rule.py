from peters_algorithm.base.asset_placement.abstract_rule import Rule
from shapely.geometry.base import BaseGeometry


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
