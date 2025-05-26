import numpy as np
from render_world import RenderWorld
from phong_shader import PhongShader
from hemi_sphere_shader import HemisphereShader
from sphere import Sphere


class Panda():
    def __init__(self, world: RenderWorld): 
        self.world = world
        self.tails = []

    def create(self, center: np.ndarray, scale: float):
        # Animal 1
        sphere_material = PhongShader(
            self.world,
            color_ambient=np.array([0.0, 0.0, 0.0]),
            color_diffuse=np.array([0.9, 0.9, 0.9]),
            color_specular=np.array([0.0, 1.0, 1.0]),
            specular_power=50
        )
        sphere_material2 = PhongShader(
            self.world,
            color_ambient=np.array([0.0, 0.0, 0.0]),
            color_diffuse=np.array([0.2, 0.2, 0.2]),
            color_specular=np.array([0.0, 1.0, 1.0]),
            specular_power=50
        )

        # body_center = np.array([-2, 0.1, 3])
        body_center = center
        body_radius = 1.0 * scale
        hemisphere_material = HemisphereShader(
            self.world,
            center=body_center,
            up_vector=np.array([0, 1, 0]),
            shader_top=sphere_material2,
            shader_bottom=sphere_material
        )
        
        body = Sphere(center=body_center, radius=body_radius, shader=hemisphere_material)
        self.world.objects.append(body)

        head_y = body_center[1] + body_radius * 0.9
        head_radius = body_radius *0.8
        head = Sphere(center=np.array([body_center[0], head_y, body_center[2]]), 
                              radius=head_radius, shader=sphere_material)
        self.world.objects.append(head)

        ear_radius = body_radius * 0.3
        ear_x_offset = body_radius * 0.7
        ear_y_offset = body_radius * 0.4
        l_ear = Sphere(center=np.array([body_center[0] + ear_x_offset, head_y + ear_y_offset, body_center[2] - ear_radius]), 
                               radius=ear_radius, shader=sphere_material2)
        self.world.objects.append(l_ear)
        r_ear = Sphere(center=np.array([body_center[0] - ear_x_offset, head_y + ear_y_offset, body_center[2] - ear_radius]),
                               radius=ear_radius, shader=sphere_material2)
        self.world.objects.append(r_ear)

        torso_radius = body_radius * 0.5
        leg_y_offset = body_radius * 0.4
        l_leg1 = Sphere(center=np.array([body_center[0] + ear_x_offset, body_center[1] - leg_y_offset, body_center[2]]), 
                        radius=torso_radius, shader=sphere_material2)
        self.world.objects.append(l_leg1)
        r_leg = Sphere(center=np.array([body_center[0] - ear_x_offset,  body_center[1] - leg_y_offset, body_center[2]]), 
                       radius=torso_radius, shader=sphere_material2)
        self.world.objects.append(r_leg)

        torso_radius2 = body_radius * 0.4
        torso_offset = body_radius * 0.1
        l_leg2 = Sphere(center=np.array([body_center[0] + body_radius, l_leg1.center[1] + torso_offset, body_center[2] + torso_offset]), 
                                radius=torso_radius2, shader=sphere_material2)
        self.world.objects.append(l_leg2)
        l_hand = Sphere(center=np.array([body_center[0] + ear_x_offset, l_leg2.center[1] + torso_radius, body_center[2] + torso_offset]), 
                                radius=torso_radius2, shader=sphere_material2)
        self.world.objects.append(l_hand)

        tail = Sphere(center=np.array([body_center[0], body_center[1] - body_radius * 0.5, body_center[2] - body_radius]), 
                                radius= body_radius * 0.2, shader=sphere_material2)
        tail0 = Sphere(center=np.array([body_center[0], body_center[1] - body_radius * 0.5, body_center[2] - body_radius]), 
                                radius= body_radius * 0.1, shader=sphere_material2)
        self.world.objects.append(tail)

        self.tails.append(tail0)
        self.tails.append(tail)

