import copy
from tqdm import tqdm
from pita_algorithm.base.world_sites.environment import Environment
from pita_algorithm.base.asset_parsing.mujoco_object import MujocoObject


class BorderPlacer:
    """Places borders into the given environment."""

    def __init__(self):
        """Constructor of the BorderPlacer class."""
        pass

    def add(
        self,
        environment: Environment,
        mujoco_object_blueprint: MujocoObject,
        amount: int = 4,
        has_border: bool = False,
    ) -> None:
        """Adds the borders around the environment.

        Parameters:
            environment (Environment): Environment class instance
            mujoco_object_blueprint (MujocoObject): Blueprint of to-be-placed mujoco object
            amount (int): Number of to-be-placed borders
            has_border (bool): True if border is added to environment, else False
        """
        if has_border:
            size = environment.size

            blueprint_x, blueprint_y, blueprint_z = (
                mujoco_object_blueprint.mjcf_obj.worldbody.body[0].geom[0].size
            )

            # Calculate border coordinates, add/sub width/breadth of the object
            # to remove overlap with the plane
            top_middle = (0, size[1] + blueprint_y)
            bottom_middle = (0, -size[1] - blueprint_y)
            right_middle = (size[0] + blueprint_x, 0)
            left_middle = (-size[0] - blueprint_x, 0)

            # Coordinates are given in halfs already
            coords = (top_middle, bottom_middle, right_middle, left_middle)

            # Load borders
            borders = [copy.deepcopy(mujoco_object_blueprint) for _ in range(amount)]

            for idx, border in tqdm(enumerate(borders)):
                border_body = border.mjcf_obj.worldbody.body[0]

                # Enlarge border on x-axis
                if coords[idx][0] == 0:
                    border_body.geom[0].size[0] = size[0]

                    border_body.pos[0] = coords[idx][0]
                    border_body.pos[1] = coords[idx][1]
                    border_body.pos[2] = blueprint_z

                # Enlarge border on y-axis
                else:
                    border_body.geom[0].size[1] = size[1]

                    border_body.pos[0] = coords[idx][0]
                    border_body.pos[1] = coords[idx][1]
                    border_body.pos[2] = blueprint_z

                environment.add(mujoco_object=border)
