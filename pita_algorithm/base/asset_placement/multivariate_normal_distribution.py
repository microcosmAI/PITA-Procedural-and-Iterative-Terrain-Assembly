import numpy as np

from pita_algorithm.base.asset_placement.abstract_placer_distribution import (
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

        Parameters:
            parameters (dict): Parameters for the multivariate normal distribution
        """
        self.mean = np.array(parameters["mean"])
        self.cov = np.array(parameters["cov"])

    def __call__(self):
        """Draws a sample from a multivariate normal distribution.

        Returns:
            sample (np.ndarray): Sampled coordinates
        """
        sample = np.random.multivariate_normal(self.mean, self.cov)

        x, y = sample

        return x, y
