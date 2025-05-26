import numpy as np
from render_world import RenderWorld
from phong_shader import PhongShader
from mesh import Mesh
from sphere import Sphere


class Cat():
    def __init__(self, world: RenderWorld): 
        self.world = world
        self.tails = []

    def create(self, center: np.ndarray, scale: float):

        orange = PhongShader(
        self.world,
        color_ambient=np.array([0.0, 0.0, 0.0]),
        color_diffuse=np.array([0.9, 0.5, 0.2]),
        color_specular=np.array([1.0, 1.0, 1.0]),
        specular_power=50
        )

        # body_center = np.array([2, 1, 3])
        body_center = center
        body_radius = 1.0 * scale

        body = Sphere(center=body_center, radius=body_radius, shader=orange)
        self.world.objects.append(body)     
        head_radius = body_radius *0.7
        head = Sphere(center=np.array([body_center[0], body_center[1] + body_radius, body_center[2]]), 
                      radius=head_radius, shader=orange)
        self.world.objects.append(head)

        ear_top_y_offset = body_radius * 0.9
        ear_nd1_y_offset = body_radius * 0.4
        ear_nd2_y_offset = body_radius * 0.7
        ear_top_x_offset = body_radius * 0.7
        ear_nd1_x_offset = body_radius * 0.6
        ear_nd2_x_offset = body_radius * 0.1
        vertices = np.array([
            [head.center[0] - ear_top_x_offset, head.center[1] + ear_top_y_offset, body_center[2]], # 0: Left Ear Top
            [head.center[0] - ear_nd1_x_offset, head.center[1] + ear_nd1_y_offset, body_center[2]], # 1: Left Ear Bottom Left
            [head.center[0] - ear_nd2_x_offset, head.center[1] + ear_nd2_y_offset, body_center[2]], # 2: Left Ear Bottom Right
            [head.center[0] + ear_top_x_offset, head.center[1] + ear_top_y_offset * 1.1, body_center[2]], # 3: Right Ear Top
            [head.center[0] + ear_nd2_x_offset, head.center[1] + ear_nd2_y_offset, body_center[2]], # 4: Right Ear Bottom Left
            [head.center[0] + ear_nd1_x_offset, head.center[1] + ear_nd1_y_offset, body_center[2]], # 5: Right Ear Bottom Right

        ], dtype=np.float32)

        triangles = np.array([
            [1, 0, 2],
            [4, 3, 5],
        ], dtype=np.int32)
        ear_mesh = Mesh(vertices, triangles, orange)
        self.world.objects.append(ear_mesh)

        leg_radius = body_radius * 0.3
        leg_offset = body_radius * 0.4
        lleg = Sphere(center=np.array([body_center[0] - body_radius * 0.75, body_center[1] - leg_offset, body_center[2] + leg_offset]), 
                      radius=leg_radius, shader=orange)
        self.world.objects.append(lleg)

        tail_radius = body_radius * 0.15
        tail_z_offset = body_radius * 0.9
        tail_y_offset = body_radius * 0.3
        tail_shift1 = body_radius * 0.1
        tail_shift2 = body_radius * 0.05
        tail1 = Sphere(center=np.array([body_center[0] + tail_shift2, body_center[1] - tail_y_offset, body_center[2] - tail_z_offset]), 
                       radius=tail_radius, shader=orange)
        tail2 = Sphere(center=np.array([body_center[0] + tail_shift1, tail1.center[1] - tail_shift1, tail1.center[2] - tail_shift1]), 
                       radius=tail_radius, shader=orange)
        tail3 = Sphere(center=np.array([tail1.center[0], tail2.center[1] - tail_shift1, tail2.center[2] - tail_shift1]), 
                       radius=tail_radius, shader=orange)
        self.world.objects.append(tail1)
        self.world.objects.append(tail2)
        self.world.objects.append(tail3)

        self.tails.append(tail1)
        self.tails.append(tail2)
        self.tails.append(tail3)


