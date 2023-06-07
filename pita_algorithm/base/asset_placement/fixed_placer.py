from pita_algorithm.base.asset_placement.validator import Validator
from pita_algorithm.base.world_sites.abstract_site import AbstractSite
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from pita_algorithm.base.asset_placement.abstract_placer import AbstractPlacer


class FixedPlacer(AbstractPlacer):
    """Places objects in a fixed manner."""

    def __init__(self):
        """Constructor of the FixedPlacer class."""
        pass

    def add(
        self,
        site: AbstractSite,
        mujoco_object_blueprint: MujocoObject,
        mujoco_object_rule_blueprint: MujocoObject,
        validators: list[Validator],
        amount: int,
        coordinates: list[list[float, float, float]],
    ):
        """Adds a mujoco object to a site by calling the sites add method
        after checking placement via the validator.

        Parameters:
            site (AbstractSite): AbstractSite class instance where the object is added to
            mujoco_object_blueprint (MujocoObject): Blueprint of to-be-placed mujoco object
            mujoco_object_rule_blueprint (MujocoObject): To-be-checked mujoco object
            validators (list[Validator]): Validator class instance used to check object placement
            coordinates (list[list[float, float, float]]): List of coordinate lists where each object is placed
        """
        for obj_idx in range(amount):
            # Set the position of the object to the user specified coordinates
            mujoco_object_rule_blueprint.position = coordinates[obj_idx]

            if not all(
                [
                    val.validate(mujoco_object=mujoco_object_rule_blueprint, site=site)
                    for val in validators
                ]
            ):
                raise RuntimeError(
                    "User specified placement of object '{}' at '{}' in site '{}' could not be satisfied.".format(
                        mujoco_object_rule_blueprint.name,
                        mujoco_object_rule_blueprint.position,
                        site.name,
                    )
                )

            # Copy the blueprint to avoid changing the original
            mujoco_object = self._copy(mujoco_object_blueprint)
            mujoco_object.position = mujoco_object_rule_blueprint.position

            # Keep track of the placement in the validators
            for validator in validators:
                validator.add(mujoco_object)

            # Add the object to the site
            site.add(mujoco_object=mujoco_object)

    def remove(self, site: AbstractSite, mujoco_object: MujocoObject):
        """Removes a mujoco object from a site by calling the sites remove method.
        Possibly checks placement via the validator.

        Parameters:
            site (Site): Site class instance where the object is removed from
            mujoco_object (MujocoObject): To-be-removed mujoco object
        """
        site.remove(mujoco_object=mujoco_object)
