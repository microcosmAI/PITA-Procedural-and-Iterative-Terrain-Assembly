from abc import ABC, abstractmethod


class Site(ABC):
    """  abstract class for environment and area functionality
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_mjcf(self):
        """ functionality to retrieve mjcf object of finished world-design of child classes """
        pass

    @abstractmethod
    def add(self):
        """ add functionality to place objects in child classes """
        pass

    @abstractmethod
    def remove(self):
        """ remove functionality to place objects in child classes """
        pass
