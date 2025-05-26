import numpy as np
from shader import Shader
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from render_world import RenderWorld
    from ray import Ray

class FlatShader(Shader):
    def __init__(self, world_input: 'RenderWorld', color: np.ndarray):
        super().__init__(world_input)
        self.color = np.array(color, dtype=float)

    def shade_surface(self, ray: 'Ray', intersection_point: np.ndarray,
                      normal: np.ndarray, recursion_depth: int) -> np.ndarray:
        return self.color