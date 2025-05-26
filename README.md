# Project Structure Overview

A clear breakdown of the project files and their responsibilities.

---

## 📦 Globals & Utilities

- **globals.py**  
  Global variables used throughout the project.

- **util.py**  
  Helper functions for various project tasks.

---

## 🌍 Core World Elements

- **camera.py**  
  Camera class for scene viewing.

- **render_world.py**  
  Handles world rendering logic.

- **ray.py**  
  Ray tracing and ray-related operations.

---

## 💡 Lighting

- **light.py**  
  Base class for light sources.

- **point_light.py**  
  Implementation of point light sources.

---

## 🎨 Shader Classes

- **shader.py**  
  Base shader class.

- **sky_shader.py**  
  Sky shader using spherical coordinates to sample colors from an image.

- **texture_shader.py**  
  Shader that samples pixel colors from a selected image.

- **hemi_sphere_shader.py**  
  Shades a hemisphere black or white based on Y value relative to the center.

- **flat_shader.py**  
  Simple flat color shader.

- **phong_shader.py**  
  Shader implementing the Phong ray tracing effect.

---

## 🐾 Animation & Movement

- **forward_kinematics.py**  
  Handles object tail wagging and forward kinematics.

---

## ⚡ Lightning Effects

- **lightning_segment.py**  
  Represents segments of lightning.

- **lightning_shader.py**  
  Shader for rendering lightning effects.

- **lightning.py**  
  Main logic for lightning effects.

---

## 🧩 Object Creation

- **object.py**  
  Base class for all objects.

- **cat.py**  
  Cat object implementation.

- **panda.py**  
  Panda object implementation.

- **hill.py**  
  Hill object implementation.

- **mesh.py**  
  Mesh object implementation.

- **plane.py**  
  Plane object implementation.

- **sphere.py**  
  Sphere object implementation.

---

## 🚀 Entry Point

- **main.py**  
  Main entry point of the project.
