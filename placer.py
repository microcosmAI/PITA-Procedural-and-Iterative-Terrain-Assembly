from abc import ABC, abstractmethod
from dm_control import mjcf
import Validator
import Site


class Placer(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add(
        self, site: Site, mujoco_object: mjcf.RootElement, validator: list[Validator]
    ):
        site.add(mujoco_object)

    @abstractmethod
    def remove(self, site: Site, mujoco_object: mjcf.RootElement):
        site.remove(mujoco_object)
