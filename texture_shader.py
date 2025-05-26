import numpy as np
from shader import Shader
from PIL import Image
from ray import Ray
import math

class TextureShader(Shader):
    def __init__(self, world, color_ambient, color_specular, specular_power, path):
        super().__init__(world)
        self.color_ambient = color_ambient
        self.image = Image.open(path).convert("RGB")
        self.texture = np.array(self.image) / 255.0
        self.height, self.width, _ = self.texture.shape
        self.color_specular = color_specular
        self.specular_power = specular_power

    def get_uv_coordinates(self, intersection_point: np.ndarray): # simple version just make it repeat
        u = (intersection_point[0] % 1.0)
        v = (intersection_point[1] % 1.0)
        return u, v

    def shade_surface(self, ray: Ray, intersection_point: np.ndarray, normal: np.ndarray, recursion_depth: int):
        color = self.world.ambient_color * self.world.ambient_intensity * self.color_ambient

        for light in self.world.lights:
            vector_to_light = light.position - intersection_point
            light_dir = light_dir = vector_to_light / np.linalg.norm(vector_to_light)

            if self.world.enable_shadows:
                ray_shadow = Ray(intersection_point, light_dir)
                hit = self.world.closest_intersection(ray_shadow)
                if hit.object and hit.dist < np.linalg.norm(vector_to_light):
                    continue

            # Diffuse component
            diffuse_intensity = max(np.dot(light_dir, normal), 0.0)
            u, v = self.get_uv_coordinates(intersection_point)
            x = min(int(u * self.width), self.width - 1)
            y = min(int(v * self.height), self.height - 1)
    
            color_diffuse = self.texture[y, x]
            diffuse = color_diffuse * diffuse_intensity * light.emitted_light(vector_to_light)

            # Specular component
            reflection_dir = 2 * np.dot(light_dir, normal) * normal - light_dir
            reflection_dir = reflection_dir / np.linalg.norm(reflection_dir)

            view_dir = self.world.camera.position - intersection_point
            view_dir = view_dir / np.linalg.norm(view_dir)
            base = max(np.dot(reflection_dir, view_dir), 0.0)
            specular_intensity = math.pow(base, self.specular_power)
            reflection = self.color_specular * specular_intensity * light.emitted_light(vector_to_light)

            color += diffuse + reflection

        return color
