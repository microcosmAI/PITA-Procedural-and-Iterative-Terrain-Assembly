from abc import ABC, abstractmethod
from dm_control import mjcf
import Environment
import Site


class Placer(ABC):
    @abstractmethod
    def __init__(self, environment: Environment):
        self.environment = environment

    @abstractmethod
    def add(self, site: Site, mujoco_object: mjcf):
        site.add(mujoco_object)

    @abstractmethod
    def remove(self, site: Site, mujoco_object: mjcf):
        site.remove(mujoco_object)
