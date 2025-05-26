import numpy as np
from abc import ABC, abstractmethod

class Light(ABC):
    def __init__(self, position=np.zeros(3), color=np.ones(3), brightness=1.0):
        self.position = np.array(position)
        self.color = np.array(color)
        self.brightness = brightness

    @abstractmethod
    def emitted_light(self, vector_to_light: np.ndarray) -> np.ndarray:
        pass
