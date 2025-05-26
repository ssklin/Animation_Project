from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from Render_world import RenderWorld  
    from Ray import Ray  

class Shader(ABC):
    def __init__(self, world_input: 'RenderWorld'):
        self.world = world_input

    @abstractmethod
    def shade_surface(self, ray: 'Ray', intersection_point: np.ndarray, normal: np.ndarray, recursion_depth: int) -> np.ndarray:
        pass
