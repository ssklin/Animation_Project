import numpy as np
from util import lerp
from lightning_segment import LightningSegment

class Lightning:
    def __init__(self, start, end, steps=30, max_shift=0.8, world=None):
        self.start, self.end, self.steps, self.max_shift = start, end, steps, max_shift
        self.world = world
        self.x, self.y, self.z = self._generate_path()
        self.segments = self._create_segments()

    def _create_segments(self):
        segments = []
        points = np.column_stack((self.x, self.y, self.z))
        for i in range(len(points) - 1):
            segment = LightningSegment(points[i], points[i + 1], self.world)
            segments.append(segment)
        return segments

    def _generate_path(self):
        x0, y0, z0 = self.start
        x1, y1, z1 = self.end
        x_points = [x0]
        y_points = [y0]
        z_points = [z0]
        dir_vec = np.array([x1 - x0, y1 - y0, z1 - z0])
        dir_norm = dir_vec / np.linalg.norm(dir_vec)
        for time in range(0, self.steps):
            percentage = time / self.steps
            x = lerp(x0, x1, percentage)
            y = lerp(y0, y1, percentage)
            z = lerp(z0, z1, percentage)

            # Add small random variations
            rand_vec = np.random.randn(3)
            perp_vec = np.cross(dir_norm, rand_vec)
            if np.linalg.norm(perp_vec) < 1e-6:
                perp_vec = np.cross(dir_norm, [1, 0, 0])
            perp_vec = perp_vec / np.linalg.norm(perp_vec)
            offset = np.random.uniform(-self.max_shift, self.max_shift) * (1 - percentage)
            x += perp_vec[0] * offset
            # y += perp_vec[1] * offset
            z += perp_vec[2] * offset * 0.5
            x_points.append(x)
            y_points.append(y)
            z_points.append(z)
        x_points.append(x1)
        y_points.append(y1)
        z_points.append(z1)
        return np.array(x_points), np.array(y_points), np.array(z_points)
