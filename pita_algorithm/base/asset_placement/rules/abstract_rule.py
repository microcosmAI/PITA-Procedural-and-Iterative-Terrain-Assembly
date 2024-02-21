from abc import ABC, abstractmethod
from shapely.geometry.base import BaseGeometry
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class Rule(ABC):
    """Abstract class for rules."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(
        self,
        map_2D: dict,
        shape_object: BaseGeometry,
        mujoco_object: MujocoObject,
        site: AbstractSite,
    ) -> bool:
        """Check if the rule is satisfied.

        Parameters:
            map_2D (dict): Dict mapping object classes to a list of their shapely representations
            shape_object (BaseGeometry): A Shapely Polygon object representing the shape to be checked
            mujoco_object (MujocoObject): The new object, that will be evaluated
            site (AbstractSite): AbstractSite class instance where the object is added to
        """
        pass
