from shader import Shader
from ray import Ray
import math
import numpy as np

class PhongShader(Shader):
    def __init__(self, world, color_ambient, color_diffuse, color_specular, specular_power):
        super().__init__(world)
        self.color_ambient = color_ambient
        self.color_diffuse = color_diffuse
        self.color_specular = color_specular
        self.specular_power = specular_power

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
            diffuse = self.color_diffuse * diffuse_intensity * light.emitted_light(vector_to_light)

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
