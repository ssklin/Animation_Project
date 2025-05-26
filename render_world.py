import numpy as np
from ray import Ray
from camera import Camera
from object import Hit
 
class RenderWorld:
    def __init__(self):
        self.camera = Camera()
        self.background_shader = None 
        self.objects = [] 
        self.lights = []  
        self.ambient_color = np.zeros(3)  
        self.ambient_intensity = 0
        self.enable_shadows = True
        self.recursion_depth_limit = 3

    def closest_intersection(self, ray: 'Ray') -> 'Hit':
        closest_hit = Hit(None, 0, 0)
        closest_dist = float('inf')

        for obj in self.objects:
            cur_hit = obj.intersection(ray, -1)

            if cur_hit.object and cur_hit.dist >= 1e-6 and (not closest_hit.object or cur_hit.dist < closest_dist):
                closest_hit = cur_hit
                closest_dist = cur_hit.dist

        return closest_hit

    def render_pixel(self, pixel_index: tuple):
        ray = Ray()
        ray.endpoint = self.camera.position

        # Find the position of the pixel in world coordinates
        pixel_position = self.camera.world_position(pixel_index)
        ray.direction = (pixel_position - self.camera.position) / np.linalg.norm(pixel_position - self.camera.position)  # Unit vector

        color = self.cast_ray(ray, self.recursion_depth_limit)
        self.camera.set_pixel(pixel_index, pixel_color(color))

    def render(self):        
        for j in range(self.camera.number_pixels[1]):
            for i in range(self.camera.number_pixels[0]):
                self.render_pixel((i, j))

    def cast_ray(self, ray: "Ray", recursion_depth: int) -> np.ndarray:
        color = np.zeros(3)  # Initialize color as black (0, 0, 0)

        if recursion_depth <= 0:
            intersection_point = np.zeros(3)
            normal = np.zeros(3)
            return self.background_shader.shade_surface(ray, intersection_point, normal, recursion_depth)

        closest_hit = self.closest_intersection(ray)

        if closest_hit.object:
            intersection_point = ray.endpoint + ray.direction * closest_hit.dist
            normal = closest_hit.object.normal(intersection_point, closest_hit.part)
            color = closest_hit.object.material_shader.shade_surface(ray, intersection_point, normal, recursion_depth)
        else:
            intersection_point = np.zeros(3)
            normal = np.zeros(3)
            color = self.background_shader.shade_surface(ray, intersection_point, normal, recursion_depth)

        return color

# Helper functions to handle Pixel color encoding and decoding
def pixel_color(color: np.ndarray) -> int:
    r = min(color[0], 1.0) * 255
    g = min(color[1], 1.0) * 255
    b = min(color[2], 1.0) * 255
    return (int(r) << 24) | (int(g) << 16) | (int(b) << 8) | 0xFF

def from_pixel(pixel: int) -> np.ndarray:
    return np.array([
        (pixel >> 24),
        (pixel >> 16) & 0xFF,
        (pixel >> 8) & 0xFF
    ]) / 255.0
