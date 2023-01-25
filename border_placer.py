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
        self, environment: Environment, mujoco_object: mjcf.RootElement, amount: int = 4
    ):
        """
        Adds the borders around the environment

        Parameters:
            environment (Environment): Environment class instance
            mujoco_object (mjcf.RootElement): To-be-placed mujoco object
            amount (int): Number of to-be-placed borders

        Returns:
            mjcf_model (mjcf): An empty environment with borders around it
        """
        # TODO Account for height value i.e. not in the ground
        size = environment.size

        # Coordinates are given in halfs already
        coords = ((0, size[1]), (0, -size[1]), (size[0], 0), (-size[0], 0))

        borders = [copy.deepcopy(mujoco_object) for _ in range(amount - 1)]
        borders.append(mujoco_object)

        for idx, border in enumerate(borders):
            border_body = border.worldbody.body[0]

            if coords[idx][0] == 0:
                border_body.geom[0].size[0] = size[0]

                border_body.pos[0] = coords[0]
                border_body.pos[1] = coords[1]

            else:
                border_body.geom[0].size[1] = size[1]

                border_body.pos[0] = coords[0]
                border_body.pos[1] = coords[1]

            environment.add(border)
