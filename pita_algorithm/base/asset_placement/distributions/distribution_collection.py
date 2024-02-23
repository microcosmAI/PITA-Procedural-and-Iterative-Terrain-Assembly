import logging
import numpy as np
from pita_algorithm.base.asset_placement.distributions.abstract_placer_distribution import (
    AbstractPlacerDistribution,
)


class MultivariateNormalDistribution(AbstractPlacerDistribution):
    """A multivariate normal distribution. The distribution is defined by the mean values
    for each dimension and the covariance matrix. The covariance matrix controls the shape,
    orientation, and spread of the distribution.

    The covariance matrix is a symmetric matrix that describes the relationship between variables
    in a multivariatenormal distribution. It provides information about the variances and covariances
    of the variables.

    - Diagonal Covariance Matrix:
      If the covariance matrix is diagonal, it means that the variables are uncorrelated, and each
      variable's variance is independent of the others.

    - Non-Diagonal Covariance Matrix:
      If the covariance matrix is non-diagonal, it means that the variables are correlated.
      The off-diagonal elements represent the covariance between the variables.
      The distribution can be rotated by introducing non-zero off-diagonal elements.

    - Scaling Covariance Matrix:
      You can scale the covariance matrix to control the spread of the distribution.
      Increasing the values on the diagonal will increase the variances,
      resulting in a wider distribution.
    """

    def __init__(self, parameters: dict):
        """Constructor of the MultivariateNormalDistribution class.

        Note: default values are "mean" [0, 0] and "cov" [site_length,     0     ]
                                                         [     0     , site_width]

        Parameters:
            parameters (dict): Parameters for the multivariate normal distribution
        """
        super().__init__(parameters=parameters)
        self.mean = np.array(parameters["mean"]) if "mean" in parameters else [0, 0]
        self.cov = (
            np.array(parameters["cov"])
            if "cov" in parameters
            else [[parameters["site_sizes"][0], 0], [0, parameters["site_sizes"][1]]]
        )
        logger = logging.getLogger()
        logger.info(
            f"Initializing MultivariateNormalDistribution with parameters {parameters}"
        )

    def __call__(self) -> (float, float):
        """Draws a sample from a multivariate normal distribution.

        Returns:
            sample (np.ndarray): Sampled coordinates
        """
        sample = np.random.multivariate_normal(self.mean, self.cov)
        x, y = sample

        return x, y


class MultivariateUniformDistribution(AbstractPlacerDistribution):
    """Multivariate uniform distribution."""

    def __init__(self, parameters: dict):
        """Constructor of the MultivariateUniform class.

        Note: default values are "low": [-site.size[0], -site.size[1]], "high": [site.size[0], site.size[1]],

        Parameters:
            parameters (dict): Parameters for the multivariate uniform distribution
        """
        super().__init__(parameters=parameters)
        self.low = (
            parameters["low"]
            if "low" in parameters
            else [-parameters["site_sizes"][0], -parameters["site_sizes"][1]]
        )
        self.high = (
            parameters["high"]
            if "high" in parameters
            else [[parameters["site_sizes"][0]], [parameters["site_sizes"][1]]]
        )
        logger = logging.getLogger()
        logger.info(
            f"Initializing MultivariateUniformDistribution with parameters {parameters}"
        )

    def __call__(self) -> (float, float):
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


class RandomWalkDistribution(AbstractPlacerDistribution):
    """Random walk distribution for object placement on a 2D plane."""

    def __init__(self, parameters: dict):
        """Constructor of the RandomWalkDistribution class.

        Note: default values are "step_size_range": [5, 10], "bounds": [-site.size[0],
                                                                        site.size[0],
                                                                        -site.size[1],
                                                                        site.size[1]],

        Parameters:
            parameters (dict): Parameters for the random walk distribution
                parameters["step_size_range"]: (min_step_size, max_step_size) - Range of step sizes
                parameters["bounds"]: (min_x, max_x, min_y, max_y) - Bounds of the 2D plane
        """
        super().__init__(parameters=parameters)
        self.step_size_range = (
            parameters["step_size_range"]
            if "step_size_range" in parameters
            else [5, 10]
        )
        self.bounds = (
            parameters["bounds"]
            if "bounds" in parameters
            else [
                -parameters["site_sizes"][0],
                parameters["site_sizes"][0],
                -parameters["site_sizes"][1],
                parameters["site_sizes"][1],
            ]
        )
        self.current_x = parameters["current_x"] if "current_x" in parameters else 0.0
        self.current_y = parameters["current_y"] if "current_y" in parameters else 0.0
        logger = logging.getLogger()
        logger.info(f"Initializing RandomWalkDistribution with parameters {parameters}")

    def __call__(self) -> (float, float):
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


class CircularUniformDistribution(AbstractPlacerDistribution):
    """Circular uniform distribution."""

    def __init__(self, parameters: dict):
        """Constructor of the CircularUniformDistribution class.

        Note: default values are "loc": 0.0, "scale": min(site.size[0], site.size[1])

        Parameters:
            parameters (dict): Parameters for the circular uniform distribution
        """
        super().__init__(parameters=parameters)
        self.loc = parameters["loc"] if "loc" in parameters else 0.0
        self.scale = (
            parameters["scale"]
            if "scale" in parameters
            else min(parameters["site_sizes"][0], parameters["site_sizes"][1])
        )
        logger = logging.getLogger()
        logger.info(
            f"Initializing CircularUniformDistribution with parameters {parameters}"
        )

    def __call__(self) -> (float, float):
        """Draws a 2D sample from a circular uniform distribution.

        Returns:
            x, y (float, float): Sampled x and y coordinates
        """
        length = np.sqrt(np.random.uniform(self.loc, self.scale**2))
        angle = np.pi * np.random.uniform(0, 2)
        x = length * np.cos(angle)
        y = length * np.sin(angle)

        return x, y
