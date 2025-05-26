from shader import Shader
from ray import Ray
import math
import numpy as np

class HemisphereShader(Shader):
    def __init__(self, world, center, up_vector, shader_top: Shader, shader_bottom: Shader):
        super().__init__(world)
        self.center = center
        self.up_vector = up_vector / np.linalg.norm(up_vector)
        self.shader_top = shader_top
        self.shader_bottom = shader_bottom

    def shade_surface(self, ray: Ray, intersection_point: np.ndarray, normal: np.ndarray, recursion_depth: int) -> np.ndarray:

        relative_pos = intersection_point - self.center
        dot_product = np.dot(relative_pos, self.up_vector)

        if dot_product >= 0:
            return self.shader_top.shade_surface(ray, intersection_point, normal, recursion_depth)
        else:
            return self.shader_bottom.shade_surface(ray, intersection_point, normal, recursion_depth)