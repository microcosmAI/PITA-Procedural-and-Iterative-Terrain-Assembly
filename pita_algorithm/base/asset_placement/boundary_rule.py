from shapely.geometry import Polygon, Point

from pita_algorithm.base.asset_placement.abstract_rule import Rule
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class BoundaryRule(Rule):
    """A rule that checks if an object is within the given boundaries."""

    def __init__(self, boundary: tuple):
        """Constructor of the Boundary Rule.

        Parameters:
            boundary (tuple): A tuple of boundary values in the format (x, y)
        """
        self.boundary = Polygon(
            [
                (-boundary[0], -boundary[1]),
                (-boundary[0], boundary[1]),
                (boundary[0], boundary[1]),
                (boundary[0], -boundary[1]),
            ]
        )

    def __call__(
        self,
        map_2D: dict,
        shape_object: Polygon,
        mujoco_object: MujocoObject,
        site: AbstractSite,
    ) -> bool:
        """Check if a given shape is within the boundary. Only utilizes the shape polygon.

        Parameters:
            map_2D (dict): Dict mapping object classes to a list of their shapely representations
            shape_object (Polygon): A Shapely Polygon object representing the shape to be checked
            mujoco_object (MujocoObject): The new object, that will be evaluated
            site (AbstractSite): AbstractSite class instance where the object is added to

        Returns:
            (bool): True if the shape is within the boundary, False otherwise
        """
        if isinstance(shape_object, Point):
            return self.boundary.contains(shape_object)
        else:
            return self.boundary.intersects(shape_object)
