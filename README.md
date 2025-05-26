---

globals.py: global variables
util.py: helping function for the project

---

Class for basic element to create the world:

camera.py
render_world.py
ray.py

---

World light:
light.py
point_light.py

---

Shader class:
shader.py
sky_shader.py: A shader for the sky that uses a spherical coordinate system to extract color from a selected image.
texture_shader.py: A shader that extracts color from the corresponding pixel in a selected image.
hemi_sphere_shader.py: A shader that paints a sphere in black and white depending on the relative Y value to the center.
flat_shader.py: A shader for plain color.
phong_shader.py: A shader which applies ray tracing effect.

---

class for object tail wagging:
forward_kinematics.py

---

class for lightening:
lightning_segment.py
lightning_shader.py
lightning.py

---

class for creating objects:
object.py
cat.py
panda.py
hill.py
mesh.py
object.py
plane.py
sphere.py

---

main.py
