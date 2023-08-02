import numpy as np
import matplotlib.pyplot as plt

from pita_algorithm.base.asset_placement.abstract_placer_distribution import (
    AbstractPlacerDistribution,
)


class RandomWalkDistribution(AbstractPlacerDistribution):
    """Random walk distribution for object placement on a 2D plane."""

    def __init__(self, parameters: dict):
        """Constructor of the RandomWalkDistribution class.

        Parameters:
            parameters (dict): Parameters for the random walk distribution
                parameters["step_size_range"]: (min_step_size, max_step_size) - Range of step sizes
                parameters["bounds"]: (min_x, max_x, min_y, max_y) - Bounds of the 2D plane
        """
        self.step_size_range = parameters["step_size_range"]
        self.bounds = parameters["bounds"]
        self.current_x, self.current_y = 0.0, 0.0

    def __call__(self) -> tuple[float, float]:
        """Generates the next random object placement using a random walk.

        Returns:
            (x, y) coordinates: Next randomly generated object placement
        """
        # Randomly choose the step size from the given range
        step_size = np.random.uniform(self.step_size_range[0], self.step_size_range[1])

        # Randomly choose the direction of the step (random angle)
        angle = np.random.uniform(0, 2 * np.pi)
        x_step = step_size * np.cos(angle)
        y_step = step_size * np.sin(angle)

        self.current_x += x_step
        self.current_y += y_step

        # Ensure the new position stays within the defined bounds
        self.current_x = np.clip(self.current_x, self.bounds[0], self.bounds[1])
        self.current_y = np.clip(self.current_y, self.bounds[2], self.bounds[3])

        return self.current_x, self.current_y
