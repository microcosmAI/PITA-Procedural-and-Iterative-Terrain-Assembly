import numpy as np

from pita_algorithm.base.asset_placement.abstract_placer_distribution import (
    AbstractPlacerDistribution,
)


class MultivariateUniformDistribution(AbstractPlacerDistribution):
    """Multivariate uniform distribution."""

    def __init__(self, parameters: dict):
        """Constructor of the MultivariateUniform class.

        Parameters:
            parameters (dict): Parameters for the multivariate uniform distribution
        """
        self.low = parameters["low"]
        self.high = parameters["high"]

    def __call__(self):
        """Draws a 2D sample from a multivariate uniform distribution.

        Returns:
            x, y (tuple[float, float]): Sampled x and y coordinates
        """
        # Generate samples for each dimension
        samples = [
            np.round(np.random.uniform(low=low, high=high, size=1)[0], 4)
            for low, high in zip(self.low, self.high)
        ]

        x, y = samples

        return x, y
