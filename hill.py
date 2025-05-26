import numpy as np
from sphere import Sphere
from shader import Shader

class Hill(Sphere):
    def __init__(self, center: np.ndarray, radius: float, shader: Shader):
        super().__init__(center, radius, shader)
