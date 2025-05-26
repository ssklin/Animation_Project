import numpy as np
from shader import Shader
from PIL import Image

class SkyShader(Shader):
    def __init__(self, path):
        # self.sky_color = np.array([0.529, 0.808, 0.922])
        self.image = Image.open(path).convert("RGB")
        self.texture = np.array(self.image) / 255.0
        self.height, self.width, _ = self.texture.shape

    def shade_surface(self, ray, intersection_point, normal, recursion_depth):
        # return self.sky_color
        dir = ray.direction / np.linalg.norm(ray.direction)

        # reference: https://en.wikipedia.org/wiki/Spherical_coordinate_system
        # reference: chatGPT prompt: coorect formula for spherical coordinate transform
        theta = np.arccos(np.clip(dir[1], -1.0, 1.0))
        phi = np.arctan2(dir[2], dir[0])      

        u = (phi + np.pi) / (2 * np.pi) 
        v = theta / np.pi

        # Convert to pixel coordinates
        x = int(u * (self.width - 1))
        y = int((1 - v) * (self.height - 1))

        return self.texture[y, x]
