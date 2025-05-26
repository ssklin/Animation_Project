import numpy as np
from shader import Shader
from render_world import RenderWorld
from ray import Ray


class LightningShader(Shader):
    def __init__(self, world_input: 'RenderWorld'):
        super().__init__(world_input)
        # self.color = np.array([0.9, 0.8, 1.0])
        self.color = np.array([1.0, 1.0, 0.8])

    def shade_surface(self, ray: 'Ray', intersection_point: np.ndarray,
                      normal: np.ndarray, recursion_depth: int) -> np.ndarray:
        return self.color
