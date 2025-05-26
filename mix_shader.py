from shader import Shader
from ray import Ray
import numpy as np
import random

class MixShader(Shader):
    def __init__(self, world, shader_combination: list[Shader]):
        super().__init__(world)
        self.shader_combination = shader_combination

    def shade_surface(self, ray: Ray, intersection_point: np.ndarray, normal: np.ndarray, recursion_depth: int) -> np.ndarray:
        random_number = random.randint(0, len(self.shader_combination) - 1)

        return self.shader_combination[random_number].shade_surface(ray, intersection_point, normal, recursion_depth)