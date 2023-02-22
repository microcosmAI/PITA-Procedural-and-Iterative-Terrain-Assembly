import copy
from dm_control import mjcf

from .mujoco_object import MujocoObject
from .placer import Placer
from .validator import Validator
from .site import Site


class FixedPlacer(Placer):
    """Class for placing objects in a fixed manner"""

    def __init__(self):
        """Initializes the FixedPlacer class."""
        pass

    def _copy(self, mujoco_object_blueprint: MujocoObject) -> MujocoObject:
        """Creates a copy of a mujoco object blueprint

        Parameters:
            mujoco_object_blueprint (MujocoObject): To-be-copied mujoco object

        Returns:
            mujoco_object (MujocoObject): Copy of the mujoco object blueprint
        """
        mujoco_object = copy.deepcopy(mujoco_object_blueprint)
        # TODO NameGenerator
        # TODO modify references to relevant object attributes like size/pos
        return mujoco_object

    def add(
        self,
        *,
        site: Site,
        mujoco_object_blueprint: MujocoObject,
        validator: list[Validator]
    ):
        """Adds a mujoco object to a site by calling the sites add method.
        Possibly checks placement via the validator.

        Parameters:
            site (Site): Site class instance where the object is added to
            mujoco_object_blueprint (MujocoObject): To-be-placed mujoco object
            validator (Validator): Validator class instance used to check object placement
        """
        mujoco_object = self._copy(mujoco_object_blueprint)


        # Set the position of the object to the user specified coordinates
        mujoco_object.position = mujoco_object.coordinates

        # TODO: Create a validator class that checks if the fixed object is placed in a valid way
        # TODO: How should the coordinates be specified in the yaml file and are they correctly parsed by the parser and associated with the object?
        # TODO: Test if the fixed placer works correctly
        if not all([val.validate(mujoco_object) for val in validator]):
            raise RuntimeError(
                "User specified placement at {} could not be satisfied.".format(
                    mujoco_object.coordinates
                )
            )

        site.add(mujoco_object=mujoco_object)

    def remove(self, *, site: Site, mujoco_object: MujocoObject):
        """Removes a mujoco object from a site by calling the sites remove method.
        Possibly checks placement via the validator.

        Parameters:
            site (Site): Site class instance where the object is removed from
            mujoco_object (MujocoObject): To-be-removed mujoco object
        """
        site.remove(mujoco_object=mujoco_object)