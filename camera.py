import numpy as np
from math import tan, radians
from typing import Tuple

# Pixel = np.uint32 

class Camera:
    def __init__(self):
        self.colors = None
        self.position = np.zeros(3)
        self.film_position = np.zeros(3)
        self.look_vector = np.zeros(3)
        self.vertical_vector = np.zeros(3)
        self.horizontal_vector = np.zeros(3)
        self.min = np.zeros(2)
        self.max = np.zeros(2)
        self.image_size = np.zeros(2)
        self.pixel_size = np.zeros(2)
        self.number_pixels = np.zeros(2, dtype=int)
    
    def __del__(self):
        if self.colors is not None:
            del self.colors

    def position_and_aim_camera(self, position_input: np.ndarray, look_at_point: np.ndarray, pseudo_up_vector: np.ndarray):
        self.position = position_input
        self.look_vector = (look_at_point - self.position) / np.linalg.norm(look_at_point - self.position)
        self.horizontal_vector = np.cross(self.look_vector, pseudo_up_vector)
        self.horizontal_vector /= np.linalg.norm(self.horizontal_vector)
        self.vertical_vector = np.cross(self.horizontal_vector, self.look_vector)
        self.vertical_vector /= np.linalg.norm(self.vertical_vector)

    def focus_camera(self, focal_distance: float, aspect_ratio: float, field_of_view: float):
        self.film_position = self.position + self.look_vector * focal_distance
        width = 2.0 * focal_distance * tan(0.5 * field_of_view)
        height = width / aspect_ratio
        self.image_size = np.array([width, height])

    def set_resolution(self, number_pixels_input: Tuple[int, int]):
        self.number_pixels = np.array(number_pixels_input)
        if self.colors is not None:
            del self.colors
        self.colors = np.zeros(self.number_pixels[0] * self.number_pixels[1], dtype=np.uint32 )
        self.min = -0.5 * self.image_size
        self.max = 0.5 * self.image_size
        self.pixel_size = self.image_size / np.array(self.number_pixels, dtype=float)

    def world_position(self, pixel_index: Tuple[int, int]) -> np.ndarray:
        x, y = pixel_index
        cell_center = self.cell_center((x, y))
        return self.film_position + self.horizontal_vector * cell_center[0] + self.vertical_vector * cell_center[1]

    def cell_center(self, index: Tuple[int, int]) -> np.ndarray:
        return self.min + (np.array(index) + np.array([0.5, 0.5])) * self.pixel_size

    def set_pixel(self, pixel_index: Tuple[int, int], color: np.uint32 ):
        i, j = pixel_index
        self.colors[j * self.number_pixels[0] + i] = color

# Helper functions to handle Pixel colors
def pixel_color(color: np.ndarray) -> np.uint32 :
    r = np.minimum(color[0], 1.0) * 255
    g = np.minimum(color[1], 1.0) * 255
    b = np.minimum(color[2], 1.0) * 255
    return (int(r) << 24) | (int(g) << 16) | (int(b) << 8) | 0xFF

def from_pixel(pixel: np.uint32 ) -> np.ndarray:
    return np.array([
        (pixel >> 24) & 0xFF,
        (pixel >> 16) & 0xFF,
        (pixel >> 8) & 0xFF
    ]) / 255.0
