from shapely.geometry import Polygon, Point
from peters_algorithm.base.asset_placement.abstract_rule import Rule
from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from peters_algorithm.base.world_container.abstract_container import AbstractContainer


class BoundaryRule(Rule):
    """A rule that checks if an object is within the given boundaries."""

    def __init__(self, boundary: tuple):
        """
        Initialize the Boundary Rule

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
        map2d: dict,
        shape: Polygon,
        mujoco_object: MujocoObject,
        site: AbstractContainer,
    ) -> bool:
        """
        Check if a given shape is within the boundary.

        Parameters:
            map2d (dict): A dictionary representing a 2D map of the environment.
            shape (Polygon): A Shapely Polygon object representing the shape to be checked.
            mujoco_object (MujocoObject): The new object, that will be evaluated
            site (AbstractContainer): AbstractContainer class instance where the object is added to

        Returns:
            bool: True if the shape is within the boundary, False otherwise.
        """
        if isinstance(shape, Point):
            return self.boundary.contains(shape)
        else:
            return self.boundary.intersects(shape)
