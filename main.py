import os
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import globals
from render_world import RenderWorld
from camera import Camera
from point_light import PointLight
from hill import Hill
from texture_shader import TextureShader
from sky_shader import SkyShader
from lightning import Lightning
from lightning_segment import LightningSegment
from panda import Panda
from cat import Cat
from sphere import Sphere
from PIL import Image
from phong_shader import PhongShader
from forward_kinematics import dh_transform
from forward_kinematics import forward_kinematics_all_joints

# --- Configuration ---
# image settings
IMAGE_WIDTH = int(globals.IMG_WIDTH * globals.IMG_SCALE)
IMAGE_HEIGHT = int(globals.IMG_HEIGHT * globals.IMG_SCALE)

# animation settings
dt = 1 / globals.ANIMATION_FPS  # pause time between each animation picture
DURATION = globals.ANIMATION_DURATION  # animation time for lightning (0 ~ DURATION - 1)
LIGHTNING_STEPS = globals.ANIMATION_LIGHTNING_STEPS
LIGHTNING_DURATION = globals.ANIMATION_LIGHTNING_DURATION

# object settings (shared across functions)
panda_stone_center = globals.POSITIONS["panda_stone_center"]
panda_center = globals.POSITIONS["panda_center"]
panda_lightning_start = globals.POSITIONS["panda_lightning_start"]
panda_lightning_end = globals.POSITIONS["panda_lightning_end"]
cat_stone_center = globals.POSITIONS["cat_stone_center"]
cat_center = globals.POSITIONS["cat_center"]
cat_lightning_start = globals.POSITIONS["cat_lightning_start"]
cat_lightning_end = globals.POSITIONS["cat_lightning_end"]

def set_camera(world: 'RenderWorld'):
    '''
    Camera setup
    '''
    camera_position = np.array([0, 0, -1])
    look_at = np.array([0, 0, 0])
    pseudo_up = np.array([0, 1, 0])
    fov = 120
    aspect_ratio = IMAGE_WIDTH / IMAGE_HEIGHT
    focal_distance = 1.0

    camera = Camera()
    camera.position_and_aim_camera(camera_position, look_at, pseudo_up)
    camera.focus_camera(focal_distance, aspect_ratio, fov*(math.pi/180))
    camera.set_resolution((IMAGE_WIDTH, IMAGE_HEIGHT))
    world.camera = camera
# end def


def set_light(world: 'RenderWorld'):
    '''
    Light the world
    '''
    light_position = np.array([2, 1, -4])
    light_color = np.array([1.0, 1.0, 1.0])
    world.lights.append(PointLight(light_position, light_color, 550))
# end def

def set_extra_light(world: 'RenderWorld'):
    '''
    Shine the world
    '''
    light_position = np.array([0, 2, 2.5])
    light_color = np.array([1.0, 1.0, 1.0])
    world.lights.append(PointLight(light_position, light_color, 1550))
# end def


def set_ambient_light(world: 'RenderWorld'):
    '''
    Ambient light
    '''
    world.ambient_color = np.array([1.0, 1.0, 1.0])
    world.ambient_intensity = 1.0
    world.enable_shadows = False
    world.recursion_depth_limit = 1
# end def


def set_hill(world: 'RenderWorld'):
    hill_shader = TextureShader(
        world,
        color_ambient=np.array([0.09, 0.17, 0.09]),
        path="./assets/grass.jpg",
        color_specular=np.array([0.05, 0.05, 0.05]),
        specular_power=10
    )

    hill_center = np.array([0.0, -51.7, 5.0])
    hill_radius = 50.0
    hill = Hill(center=hill_center, radius=hill_radius, shader=hill_shader)
    world.objects.append(hill)
# end def


def convert_pixels_to_image_array(pixels, width, height):
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            # pixel_index = y * width + x
            pixel = pixels[(IMAGE_HEIGHT - y - 1) * IMAGE_WIDTH + x]
            # pixel_val = int(pixels[pixel_index])
            pixel_val = int(pixel)
            r = (pixel_val >> 24) & 0xFF
            g = (pixel_val >> 16) & 0xFF
            b = (pixel_val >> 8) & 0xFF
            img_array[y, x] = [r, g, b]
    return img_array
# end def


def get_img_path(time: int):
    return f"./{globals.OUTPUT_DIR}/output_{time}.png"


def create_images():
    # create output folder
    output_folder_path = f"./{globals.OUTPUT_DIR}"
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        
    world = RenderWorld()
    set_camera(world)
    set_ambient_light(world)
    set_light(world)
    world.background_shader = SkyShader("./assets/sky.jpg")
    set_hill(world)

    # create lightning objects with adjusted parameters
    panda_lightning = Lightning(panda_lightning_start, panda_lightning_end, LIGHTNING_STEPS, world=world)
    cat_lightning = Lightning(cat_lightning_start, cat_lightning_end, LIGHTNING_STEPS, world=world)

    # original stone
    sphere_material = TextureShader(
        world,
        color_ambient=np.array([0.09, 0.09, 0.09]),
        path="./assets/stone.jpg",
        color_specular=np.array([0.05, 0.05, 0.05]),
        specular_power=10
    )
    panda_stone = Sphere(panda_stone_center, 1.8, sphere_material)
    world.objects.append(panda_stone)
    cat_stone = Sphere(cat_stone_center, 1.8, sphere_material)
    world.objects.append(cat_stone)

    base_objects = list(world.objects)
    panda = Panda(world) 
    cat = Cat(world)
    remove_extra_light = True
    for time in range(DURATION):
        print(f"creating image for time = {time}")

        # start with a fresh copy each frame
        world.objects = list(base_objects)

        # lightning
        if time < LIGHTNING_DURATION and LIGHTNING_DURATION > 0:
            num_segments_to_show = min(LIGHTNING_STEPS, max(2, int((time + 1) / LIGHTNING_DURATION * LIGHTNING_STEPS)))
            world.objects.extend(panda_lightning.segments[:num_segments_to_show])
            world.objects.extend(cat_lightning.segments[:num_segments_to_show])
            # add extra light to simulate lightening hit stone
            if time == LIGHTNING_DURATION - 1:
                set_extra_light(world)
        
        # remove stone and add animal
        if time == LIGHTNING_DURATION + 1:
            world.objects.pop()
            world.objects.pop()
            scale = 1.0
            # Animal 1    
            panda.create(panda_center, scale)
            # Animal 2
            cat.create(cat_center, scale)
            base_objects = list(world.objects)

        # tail wagging        
        if time < DURATION and time > LIGHTNING_DURATION + 1:
            # remove extra light
            if remove_extra_light:
                world.lights.pop()
                remove_extra_light = False

            # cat tail wagging
            frame = (time - LIGHTNING_DURATION) * 10
            # frame = time * 10
            theta1 = np.deg2rad(frame)
            theta2 = np.deg2rad(frame / 2)
            theta3 = np.deg2rad(frame / 3)

            dh_params = [
                (theta1, 0.0, 0.0, np.deg2rad(-90)),
                (theta2, 0.0, 0.2, 0),
                (theta3, 0.0, 0.2, 0)
            ]

            # base_position = np.array([cat.tails[0].center[0], cat.tails[0].center[1], cat.tails[0].center[2] - scale * 0.15])
            base_position = cat.tails[0].center
            base_transform = np.eye(4)
            base_transform[:3, 3] = base_position
            
            positions = forward_kinematics_all_joints(dh_params, base_transform)

            cat.tails[0].center = positions[1]
            cat.tails[1].center = positions[2]
            cat.tails[2].center = positions[3]

            # panda tail wagging
            dh_params = [
                (theta1, 0.0, 0.0, np.deg2rad(-90)),
                (theta2, 0.0, 0.05, 0),
                (theta3, 0.0, 0.05, 0)
            ]

            base_position = panda.tails[0].center
            base_transform = np.eye(4)
            base_transform[:3, 3] = base_position
            
            positions = forward_kinematics_all_joints(dh_params, base_transform)

            panda.tails[1].center = positions[2]


        # --- Single Render Call ---
        world.render()

        # --- Convert and Display ---
        final_image_data = convert_pixels_to_image_array(
            world.camera.colors, IMAGE_WIDTH, IMAGE_HEIGHT)

        Image.fromarray(final_image_data).save(get_img_path(time))

        # Remove lightning segments after rendering
        if time < LIGHTNING_DURATION:
            # Remove all lightning segments
            world.objects = [obj for obj in world.objects if not isinstance(obj, LightningSegment)]
        
        print(f"created image for time = {time}")
    # end for
# end def


def show_images():
    fig = plt.figure()
    while plt.fignum_exists(fig.number):
        for time in range(DURATION):
            if not plt.fignum_exists(fig.number):
                break
            plt.clf()
            img = mpimg.imread(get_img_path(time))
            plt.imshow(img)
            plt.axis("off")
            plt.title(f"{time}")
            plt.pause(dt)
    plt.close(fig)
# end def


if __name__ == "__main__":
    create_images()
    show_images()
# end main
