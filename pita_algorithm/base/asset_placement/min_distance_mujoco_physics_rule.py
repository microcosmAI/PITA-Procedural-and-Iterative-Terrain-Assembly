import numpy as np
from dm_control import mjcf
from shapely.geometry.base import BaseGeometry

from pita_algorithm.base.asset_placement.abstract_rule import Rule
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class MinDistanceMujocoPhysicsRule(Rule):
    """Checks if a new object respects the minimum distance to other objects."""

    def __init__(self, distance: float):
        """Constructor of the MinDistanceMujocoPhysicsRule class.

        Parameters:
            distance (float): Minimal distance from the new object to all existing of specified type
        """
        self.distance = distance

    def __call__(
        self,
        map_2D: dict,
        shape_object: BaseGeometry,
        mujoco_object: MujocoObject,
        site: AbstractSite,
    ) -> bool:
        """Check if a new object can be placed at the specified position. Only utilizes
        mujoco_object and site. The internal mujoco physics engine to check if the new
        object has contacts inside a specified margin.

        Parameters:
            map_2D (dict): Dict mapping object classes to a list of their shapely representations
            shape_object (BaseGeometry): Insertion that should be evaluated
            mujoco_object (MujocoObject): The new object, that will be evaluated
            site (AbstractSite): AbstractSite class instance where the object is added to

        Returns:
            (bool): True if mujoco_object is far enough away from each object.
        """
        attachement_frame = site.mjcf_model.attach(mujoco_object.mjcf_obj)

        # If the attached mujoco_object is a composite object,
        # we need to set the margin of each geom to the specified distance
        for geom in attachement_frame.all_children()[0].find_all("geom"):
            geom.margin = self.distance

        # Create physics instance and get number of geom collisions
        physics = mjcf.Physics.from_mjcf_model(site.mjcf_model)
        num_contacts = physics.data.ncon

        # If there are no collisions, the object can be placed
        if num_contacts == 0:
            mujoco_object.mjcf_obj.detach()
            return True

        # If there are collisions,
        # we need to check if the object is colliding only with itself or with other objects
        else:
            all_ids = []

            # Get all ids of the geoms in the mujoco_object
            for geom in attachement_frame.all_children()[0].find_all("geom"):
                all_ids.append(
                    physics.data.geom(attachement_frame.full_identifier + geom.name).id
                )

            # Create a boolean mask indicating pairs that contain exactly one integer from the list
            # I.e. if the mask is true, the pair contains one geom from the mujoco_object
            # and one geom from another object
            mask = (
                np.isin(physics.data.contact.geom1, all_ids)
                & ~np.isin(physics.data.contact.geom2, all_ids)
            ) | (
                ~np.isin(physics.data.contact.geom1, all_ids)
                & np.isin(physics.data.contact.geom2, all_ids)
            )

            # Filter the pairs based on the mask
            remaining_contacts1 = physics.data.contact.geom1[mask]
            remaining_contacts2 = physics.data.contact.geom2[mask]

            if len(remaining_contacts1) == 0:
                mujoco_object.mjcf_obj.detach()
                return True

            else:
                mujoco_object.mjcf_obj.detach()
                return False
