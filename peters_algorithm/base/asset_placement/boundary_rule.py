from shapely.geometry import Polygon, Point
from peters_algorithm.base.asset_placement.abstract_rule import Rule

class BoundaryRule(Rule):
    """A rule that checks if an object is within the given boundaries."""

    def __init__(self, boundary):
        self.boundary = Polygon([
            (-boundary[0], -boundary[1]),
            (-boundary[0], boundary[1]),
            (boundary[0], boundary[1]),
            (boundary[0], -boundary[1])
        ])
    
    def __call__(self, map2d: dict, shape: Polygon):
        if isinstance(shape, Point):
            return self.boundary.contains(shape)
        else:
            return self.boundary.intersects(shape)

