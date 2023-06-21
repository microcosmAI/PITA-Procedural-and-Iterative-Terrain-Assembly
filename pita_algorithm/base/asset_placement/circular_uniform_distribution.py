import numpy as np

from pita_algorithm.base.asset_placement.abstract_placer_distribution import (
    AbstractPlacerDistribution,
)


class CircularUniformDistribution(AbstractPlacerDistribution):
    """Circular uniform distribution."""

    def __init__(self, parameters: dict):
        """Constructor of the CircularUniformDistribution class.

        Parameters:
            parameters (dict): Parameters for the circular uniform distribution
        """
        self.loc = parameters["loc"]
        self.scale = parameters["scale"]

    def __call__(self):
        """Draws a 2D sample from a circular uniform distribution.

        Returns:
            x, y (float, float): Sampled x and y coordinates
        """
        length = np.sqrt(np.random.uniform(self.loc, self.scale**2))
        angle = np.pi * np.random.uniform(0, 2)

        x = length * np.cos(angle)
        y = length * np.sin(angle)

        return x, y
