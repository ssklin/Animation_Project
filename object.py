import abc
import numpy as np
from ray import Ray
from shader import Shader

SMALL_T: float = 1e-4
DEBUG_PIXEL: bool = False

class Hit:
    def __init__(self, obj: 'Object', dist: float, part: int):
        self.object: 'Object' = obj
        self.dist: float = dist
        self.part: int = part


class Object(abc.ABC):
    def __init__(self):
        self.material_shader: Shader = None
        self.number_parts: int = 1

    @abc.abstractmethod
    def intersection(self, ray: 'Ray', part: int = -1) -> Hit:
        pass

    @abc.abstractmethod
    def normal(self, point: np.ndarray, part: int) -> np.ndarray:
        pass
