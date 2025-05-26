import numpy as np
from object import Object, Hit, SMALL_T
from shader import Shader
from ray import Ray


class Plane(Object):
    def __init__(self, point: np.ndarray, normal: np.ndarray, shader: Shader):
        super().__init__()
        self.point = np.array(point, dtype=float)
        norm_mag = np.linalg.norm(normal)
        if norm_mag < SMALL_T:
            self.normal_vec = np.array([0.0, 1.0, 0.0])
        else:
            self.normal_vec = np.array(normal, dtype=float) / norm_mag
        self.material_shader = shader
        self.number_parts = 1

    def intersection(self, ray: Ray, part: int) -> Hit:
        denom = np.dot(self.normal_vec, ray.direction)

        if abs(denom) < SMALL_T:
            return Hit(obj=None, dist=0.0, part=part)

        numerator = np.dot(self.normal_vec, self.point - ray.endpoint)

        t = numerator / denom

        if t >= SMALL_T:
            return Hit(obj=self, dist=t, part=part)
        else:
            return Hit(obj=None, dist=0.0, part=part)

    def normal(self, point: np.ndarray, part: int) -> np.ndarray:
        return self.normal_vec
