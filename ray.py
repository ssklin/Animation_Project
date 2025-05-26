import numpy as np

class Ray:
    def __init__(self, endpoint=np.array([0.0, 0.0, 0.0]), direction=np.array([0.0, 0.0, 1.0])):
        self.endpoint = np.array(endpoint)
        self.direction = self._normalize(direction)

    def _normalize(self, v):
        norm = np.linalg.norm(v)
        return v / norm

    def point(self, t):
        return self.endpoint + self.direction * t
