from object import Hit, Object
from ray import Ray
from lightning_shader import LightningShader
import numpy as np

class LightningSegment(Object):
    def __init__(self, p0, p1, world=None, thickness=6e-2):
        super().__init__()
        self.p0 = np.array(p0)
        self.p1 = np.array(p1)
        self.thickness = thickness
        if world:
            self.material_shader = LightningShader(world)
        else:
            self.material_shader = None

    def intersection(self, ray: Ray, part: int = -1) -> Hit:
        o = ray.endpoint
        d = ray.direction
        v = self.p1 - self.p0
        w = o - self.p0
        v_cross_d = np.cross(v, d)
        denom = np.linalg.norm(v_cross_d) ** 2
        if denom < 1e-8:
            return Hit(None, 0, 0)
        t = np.dot(np.cross(w, v), v_cross_d) / denom
        u = np.dot(np.cross(w, d), v_cross_d) / denom
        if t >= 0 and 0 <= u <= 1:
            p_ray = o + t * d
            p_seg = self.p0 + u * v
            dist = np.linalg.norm(p_ray - o)
            if np.linalg.norm(p_ray - p_seg) < self.thickness:  # hit thickness
                return Hit(self, dist, 0)
        return Hit(None, 0, 0)

    def normal(self, point, part):
        # Compute a 3D normal perpendicular to the segment (arbitrary, but stable)
        v = self.p1 - self.p0
        # Pick any vector not parallel with v
        if abs(v[0]) < 1e-5 and abs(v[1]) < 1e-5:
            reference = np.array([1, 0, 0])
        else:
            reference = np.array([0, 0, 1])
        n = np.cross(v, reference)
        return n / np.linalg.norm(n)
