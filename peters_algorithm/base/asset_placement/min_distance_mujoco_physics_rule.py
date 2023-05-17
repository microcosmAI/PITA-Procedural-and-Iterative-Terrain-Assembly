import re
import copy
from dm_control import mjcf
from shapely.geometry.base import BaseGeometry

from peters_algorithm.base.asset_placement.abstract_rule import Rule
from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from peters_algorithm.base.world_container.abstract_container import AbstractContainer


class MinDistanceRule(Rule):
    """Check if a new object respects the minimum distance to other objects, optionally of a specified type"""

    def __init__(self, dist: float, types: list([str, ...]) = []):
        """Initialize a new MinDistanceRule.

        Parameters:
            dist (float): Minimal distance from the new object to all existing of specified type
            types (list): By default all objects in the environment will be considered. Alternatively a list with names can be passed and all mjcf-objects that include any of these names are considered, only. Can be regex.
        """
        self.dist = dist

    def __call__(
        self,
        map_2D: dict,
        shape_object: BaseGeometry,
        mujoco_object: MujocoObject,
        site: AbstractContainer,
    ):
        """Check if a new object can be placed at the specified position. The mujoco physics engine is used to check if the new object is far enough away from all other objects.

        Parameters:
            map_2D (dict): Dictionary, mapping object classes to a list of their shapely 2d representations
            shape_object (BaseGeometry): Insertion that should be evaluated
            mujoco_object (MujocoObject): The new object, that will be evaluated
            site (AbstractContainer): AbstractContainer class instance where the object is added to

        Returns:
            (boolean): True if mujoco_object is far enough away from each object.
        """
        mujoco_object_copy = copy.deepcopy(mujoco_object.mjcf_obj)
        mujoco_object_copy.worldbody.body[0].add("joint")
        mujoco_object_copy.worldbody.body[0].geom[0].margin = self.dist

        site.mjcf_model.attach(mujoco_object_copy)

        physics = mjcf.Physics.from_mjcf_model(site.mjcf_model)
        num_contacts = physics.data.ncon

        mujoco_object_copy.detach()

        if num_contacts == 0:
            return True
        else:
            return False
