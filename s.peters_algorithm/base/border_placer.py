from dm_control import mjcf
import Placer
import Environment
import copy


class BorderPlacer(Placer):
    """Places borders into the given environment."""

    def __init__(self):
        """Initializes the BorderPlacer class."""

        super(BorderPlacer, self).__init__()

    def add(
        self, environment: Environment, mujoco_object_blueprint: mjcf.RootElement, amount: int = 4
    ):
        """
        Adds the borders around the environment

        Parameters:
            environment (Environment): Environment class instance
            mujoco_object_blueprint (mjcf.RootElement): Blueprint of to-be-placed mujoco object
            amount (int): Number of to-be-placed borders

        Returns:
            mjcf_model (mjcf): An empty environment with borders around it
        """
        # TODO Account for height value i.e. not in the ground
        size = environment.size

        top_middle = (0, size[1])
        bottom_middle = (0, -size[1])
        right_middle = (size[0], 0)
        left_middle = (-size[0], 0)


        # Coordinates are given in halfs already
        coords = (top_middle, bottom_middle, right_middle, left_middle)

        borders = [copy.deepcopy(mujoco_object_blueprint) for _ in range(amount)]

        for idx, border in enumerate(borders):
            border_body = border.worldbody.body[0]

            # Enlarge border on x-axis
            if coords[idx][0] == 0:
                border_body.geom[0].size[0] = size[0]

                border_body.pos[0] = coords[idx][0]
                border_body.pos[1] = coords[idx][1]

            # Enlarge border on y-axis
            else:
                border_body.geom[0].size[1] = size[1]

                border_body.pos[0] = coords[idx][0]
                border_body.pos[1] = coords[idx][1]

            environment.add(border)
