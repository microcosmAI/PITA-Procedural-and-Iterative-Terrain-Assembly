import copy
from dm_control import mjcf

from peters_algorithm.base.asset_placement.validator import Validator
from peters_algorithm.base.asset_parsing.mujoco_object import MujocoObject
from peters_algorithm.base.asset_placement.abstract_placer import AbstractPlacer
from peters_algorithm.base.world_container.abstract_container import AbstractContainer


class FixedPlacer(AbstractPlacer):
    """Class for placing objects in a fixed manner"""

    def __init__(self):
        """Initializes the FixedPlacer class."""
        pass

    def add(
        self,
        *,
        site: AbstractContainer,
        mujoco_object_blueprint: MujocoObject,
        validators: list[Validator],
        coordinates: tuple[float, float, float]
    ):
        """Adds a mujoco object to a site by calling the sites add method.
        Optionally checks placement via the validator.

        Parameters:
            site (AbstractContainer): AbstractContainer class instance where the object is added to
            mujoco_object_blueprint (MujocoObject): Blueprint of to-be-placed mujoco object
            validators (Validator): Validator class instance used to check object placement
            coordinates (list): List of coordinates where the object is placed
        """
        mujoco_object = self._copy(mujoco_object_blueprint)

        # Set the position of the object to the user specified coordinates
        mujoco_object.position = coordinates

        # TODO: Create a validator class that checks if the fixed object is placed in a valid way
        # TODO: Test if the fixed placer works correctly
        if not all([val.validate(mujoco_object) for val in validators]):
            raise RuntimeError(
                "User specified placement at {} could not be satisfied.".format(
                    mujoco_object.coordinates
                )
            )

        site.add(mujoco_object=mujoco_object)

    def remove(self, *, site: AbstractContainer, mujoco_object: MujocoObject):
        """Removes a mujoco object from a site by calling the sites remove method.
        Possibly checks placement via the validator.

        Parameters:
            site (Site): Site class instance where the object is removed from
            mujoco_object (MujocoObject): To-be-removed mujoco object
        """
        site.remove(mujoco_object=mujoco_object)
