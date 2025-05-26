import numpy as np
from light import Light

class PointLight(Light):
    def __init__(self, position: np.ndarray, color: np.ndarray, brightness: float = 1.0):
        self.position = np.array(position, dtype=float)
        self.color = np.array(color, dtype=float)
        self.brightness = brightness

    def emitted_light(self, vector_to_light: np.ndarray) -> np.ndarray:
        distance_squared = np.dot(vector_to_light, vector_to_light)
        if distance_squared == 0:
            return np.zeros(3)
        return (self.color * self.brightness) / (4 * np.pi * distance_squared)
