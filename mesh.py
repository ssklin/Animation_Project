import numpy as np
from ray import Ray
from object import Object
from object import Hit
from shader import Shader

weight_tolerance = 1e-4
small_t = 1e-6

class Mesh(Object):
    def __init__(self, vertices, triangles, shader: Shader):
        self.vertices = vertices
        self.triangles = triangles
        self.material_shader = shader
        
    def intersection(self, ray: Ray, part: int):
        hit = Hit(None, 0.0, part)

        if part < 0:
            closest_dist = float('inf')
            for i in range(len(self.triangles)):
                success, dist = self.Intersect_Triangle(ray, i)
                if success and dist < closest_dist:
                    closest_dist = dist
                    hit = Hit(self, dist, i)
        else:
            success, dist = self.Intersect_Triangle(ray, part)
            if success:
                hit = Hit(self, dist, part)

        return hit

    def normal(self, point: np.ndarray, part: int) -> np.ndarray:
        assert part >= 0
        tri = self.triangles[part]
        A, B, C = self.vertices[tri[0]], self.vertices[tri[1]], self.vertices[tri[2]]
        AB = B - A
        BC = C - B
        normal = np.cross(AB, BC)
        norm = np.linalg.norm(normal)
        return normal / norm if norm > 0 else normal

    def Intersect_Triangle(self, ray: Ray, tri: int):
        tri_indices = self.triangles[tri]
        A, B, C = self.vertices[tri_indices[0]], self.vertices[tri_indices[1]], self.vertices[tri_indices[2]]
        AB, BC, CA = B - A, C - B, A - C
        normal = self.normal(None, tri)

        denom = np.dot(ray.direction, normal)
        if abs(denom) < small_t:
            return False, None

        plane_dist = (np.dot(A, normal) - np.dot(ray.endpoint, normal)) / denom
        if plane_dist <= small_t:
            return False, None

        P = ray.endpoint + plane_dist * ray.direction

        # Edge tests
        if (np.dot(P - A, np.cross(AB, normal)) >= small_t or
            np.dot(P - B, np.cross(BC, normal)) >= small_t or
            np.dot(P - A, np.cross(CA, normal)) >= small_t):
            return False, None

        area_total = np.linalg.norm(np.cross(AB, BC))
        if area_total < small_t:
            return False, None

        CPA = np.linalg.norm(np.cross(P - C, CA)) / area_total
        APB = np.linalg.norm(np.cross(P - A, AB)) / area_total
        BPC = np.linalg.norm(np.cross(P - B, BC)) / area_total

        if CPA < -weight_tolerance or APB < -weight_tolerance or BPC < -weight_tolerance:
            return False, None

        return True, plane_dist
