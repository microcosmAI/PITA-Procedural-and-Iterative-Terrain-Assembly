from typing import Tuple
from abc import ABC, abstractmethod


class AbstractPlacerDistribution(ABC):
    """Abstract class for Placer Distributions."""

    def __init__(self, parameters: dict):
        """Constructor of the AbstractPlacerDistribution class.

        Parameters:
            parameters (dict): Parameters for the placer distribution
        """
        pass

    @abstractmethod
    def __call__(self) -> Tuple[float, float]:
        """Draws a 2D sample from the distribution.

        Returns:
            Tuple[float, float]: Sampled x and y coordinates
        """
        pass
