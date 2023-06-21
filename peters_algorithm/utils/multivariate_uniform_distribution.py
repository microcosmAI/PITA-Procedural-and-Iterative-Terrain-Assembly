import numpy as np


class MultivariateUniform:
    """Generates a multivariate uniform distribution.

    Parameters:
        ranges (list[tuple]): Each tuple defines the range (low, high) for one dimension

    Returns:
        x, y (tuple[float, float]): Sampled x and y coordinates
    """

    def __call__(self, ranges: list[tuple]) -> tuple[np.ndarray, np.ndarray]:
        # Generate samples for each dimension
        samples = [
            np.round(np.random.uniform(low=low, high=high, size=1)[0], 4)
            for low, high in ranges
        ]

        x, y = samples

        return x, y
