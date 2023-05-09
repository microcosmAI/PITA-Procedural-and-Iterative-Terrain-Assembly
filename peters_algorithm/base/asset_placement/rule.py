from abc import ABC, abstractmethod
from shapely.geometry.base import BaseGeometry

class Rule(ABC):
    """Abstract class for rules."""

    @abstractmethod
    def __call__(self, map2d: dict, shape: BaseGeometry):
        pass