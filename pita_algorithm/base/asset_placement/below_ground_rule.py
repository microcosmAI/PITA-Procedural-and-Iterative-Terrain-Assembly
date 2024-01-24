from shapely.geometry.base import BaseGeometry

from pita_algorithm.base.asset_placement.abstract_rule import Rule
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class GroundRule(Rule):
    """A rule that checks if an object is above ground."""

    def __init__(self, ground_level: float):
        """Constructor of the Boundary Rule.

        Parameters:
            boundary (tuple): A tuple of boundary values in the format (x, y)
        """
        self.ground_level = ground_level

    def __call__(
        self,
        map_2D: dict,
        shape_object: BaseGeometry,
        mujoco_object: MujocoObject,
        site: AbstractSite,
    ) -> bool:
        """Check if a given object is above ground. Only utilizes the shape polygon.

        Parameters:
            map_2D (dict): Dict mapping object classes to a list of their shapely representations
            shape_object (Polygon): Insertion that should be evaluated
            mujoco_object (MujocoObject): The new object, that will be evaluated
            site (AbstractSite): AbstractSite class instance where the object is added to

        Returns:
            (bool): True if the object is above ground, False otherwise
        """
        # print(map_2D)
        # print(mujoco_object.name)
        # print(mujoco_object.size)
        if self.ground_level <= mujoco_object.position[2]:
            return True
        else:
            return False
