import math
import numpy as np

from ray import Ray
from object import Hit
from object import Object
from shader import Shader

# --- Constants ---
SMALL_T = 1e-6

class Sphere(Object):
    def __init__(self, center: np.ndarray, radius: float, shader: Shader):
        self.center = np.array(center, dtype=float)
        self.radius = max(0.0, float(radius))
        self.material_shader = shader

    def intersection(self, ray: Ray, part: int) -> Hit:
        co = ray.endpoint - self.center # Vector from sphere center to ray origin

        dot_u_co = np.dot(ray.direction, co)
        dot_co_co = np.dot(co, co)

        discriminant_simplified = dot_u_co**2 - dot_co_co + self.radius**2

        if discriminant_simplified < 0:
            return Hit(obj=None, dist=0.0, part=part)

        sqrt_discriminant = math.sqrt(discriminant_simplified)
        t1 = -dot_u_co - sqrt_discriminant
        t2 = -dot_u_co + sqrt_discriminant

        t = 0.0
        valid_hit = False
        if t1 >= SMALL_T:
            t = t1
            valid_hit = True
        elif t2 >= SMALL_T:
            t = t2
            valid_hit = True

        if valid_hit:
            return Hit(obj=self, dist=t, part=part)
        else:
            return Hit(obj=None, dist=0.0, part=part)

    def normal(self, point: np.ndarray, part: int) -> np.ndarray:
        normal_vec = point - self.center
        norm = np.linalg.norm(normal_vec)

        return normal_vec / norm