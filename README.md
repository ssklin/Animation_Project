# Project Documentation: 3D Animation Engine

This project is a Python-based 3D rendering engine designed to create an animation. It utilizes ray tracing techniques to generate images, with support for various geometric primitives, shaders, lighting, and animation capabilities.

## I. Core Rendering Engine

These files form the foundational components of the 3D rendering pipeline.

*   **`render_world.py`**:
    *   **Purpose**: This is a central class that manages the entire 3D scene. It holds references to the camera, all objects in the scene, light sources, and global rendering settings like ambient light, shadow enabling, and recursion depth for ray tracing. Its `render()` method orchestrates the process of shooting rays for each pixel and determining the final color. The `cast_ray()` method is crucial for tracing individual rays and handling intersections and shading.
*   **`camera.py`**:
    *   **Purpose**: Defines the virtual camera used to view the 3D scene. It handles camera positioning, orientation (look-at point, up vector), field of view, aspect ratio, focal distance, and resolution. It's responsible for calculating the world-space position corresponding to each pixel on the image plane and storing the rendered pixel colors.
*   **`ray.py`**:
    *   **Purpose**: Defines a 3D ray, which is fundamental to ray tracing. A ray is characterized by an origin (endpoint) and a normalized direction vector. It includes a method to calculate a point along the ray given a distance `t`.
*   **`object.py`**:
    *   **Purpose**: This file defines an abstract base class (`Object`) for all renderable objects in the scene. It mandates that all concrete object types (like spheres, planes) must implement `intersection()` (to test if a ray hits the object) and `normal()` (to get the surface normal at a hit point) methods. It also includes a `Hit` class to store information about a ray-object intersection.
*   **`light.py`**:
    *   **Purpose**: Defines an abstract base class (`Light`) for different types of light sources in the scene. It establishes a common interface for lights, requiring them to implement an `emitted_light()` method, which calculates the light intensity and color contributed by the light source at a given point.
*   **`point_light.py`**:
    *   **Purpose**: Implements a specific type of light source: a point light. A point light emits light uniformly in all directions from a single point in space. The intensity of the light attenuates with distance from the light source.
*   **`shader.py`**:
    *   **Purpose**: Defines an abstract base class (`Shader`) for material properties and lighting calculations. Shaders determine how an object's surface reacts to light. All concrete shader types must implement a `shade_surface()` method, which calculates the color of a point on an object's surface given the incoming ray, intersection point, surface normal, and recursion depth.

## II. Geometric Primitives & Scene Elements

These files define the shapes and specific visual elements that can be placed in the 3D world.

*   **`sphere.py`**:
    *   **Purpose**: Implements a sphere object, inheriting from the `Object` base class. It includes logic for calculating ray-sphere intersections and determining the surface normal at any point on the sphere.
*   **`plane.py`**:
    *   **Purpose**: Implements an infinite plane object, inheriting from `Object`. It provides methods for ray-plane intersection tests and calculating the plane's normal vector.
*   **`mesh.py`**:
    *   **Purpose**: (Assuming standard functionality based on the name, as the content was not provided) This file would typically define a mesh object, which is a collection of vertices, edges, and faces (usually triangles) that make up a more complex 3D shape. It would handle ray-triangle intersections for each face in the mesh.
*   **`hill.py`**:
    *   **Purpose**: Defines a `Hill` object. Interestingly, it inherits from `Sphere`, suggesting that hills in this project are represented as large spheres, likely to create a rolling landscape.
*   **`lightning_segment.py`**:
    *   **Purpose**: Represents a single segment of a lightning bolt as a 3D object. It likely models the segment as a cylinder or a line with thickness and provides methods for ray intersection with this segment and calculating its normal. It uses a `LightningShader` for its appearance.

## III. Shaders (Materials & Visual Effects)

These files define how the surfaces of objects look and react to light.

*   **`phong_shader.py`**:
    *   **Purpose**: Implements the Phong shading model. This is a common lighting model that calculates the color of a surface by combining ambient, diffuse, and specular lighting components, resulting in more realistic-looking surfaces with highlights.
*   **`texture_shader.py`**:
    *   **Purpose**: Implements texture mapping. This shader allows 2D images (textures) to be wrapped around 3D objects. It calculates UV coordinates for a point on the surface and samples the texture image to determine the diffuse color, which is then combined with lighting calculations.
*   **`flat_shader.py`**:
    *   **Purpose**: Implements a very simple flat shading model. Objects using this shader will be rendered with a uniform color across their entire surface, without any lighting calculations affecting the base color.
*   **`sky_shader.py`**:
    *   **Purpose**: Implements a shader for the background or sky. It uses a texture image (a skybox or skydome texture) and maps the direction of rays that don't hit any object to a color from this texture, creating a sky-like background.
*   **`lightning_shader.py`**:
    *   **Purpose**: A specialized shader designed specifically for rendering lightning bolts. It likely returns a bright, emissive color to make the lightning segments glow.
*   **`hemi_sphere_shader.py`**:
    *   **Purpose**: A shader that applies two different sub-shaders to an object based on the surface normal's orientation relative to an "up" vector and the object's center. This allows, for example, the top half of a sphere to have a different material/color than its bottom half.
*   **`mix_shader.py`**:
    *   **Purpose**: This shader takes a list of other shaders and, when `shade_surface` is called, randomly selects one of the shaders from the list to determine the surface color. This can be used to create varied or mottled surface appearances.

## IV. Animation & Kinematics

These files deal with making objects move or change over time.

*   **`forward_kinematics.py`**:
    *   **Purpose**: Provides functions for forward kinematics calculations. This is used to determine the position and orientation of segments in an articulated structure (like an arm or a tail) based on joint angles and segment lengths, using Denavit-Hartenberg (DH) parameters.
*   **`lightning.py`**:
    *   **Purpose**: (Assuming standard functionality based on the name and usage in `main.py`, as the content was not provided) This file would manage the creation and animation of a complete lightning bolt effect. It likely generates a series of connected `LightningSegment` objects, possibly using a procedural algorithm (like a random walk or L-system) to create the characteristic jagged path of lightning. It would also handle the timing and appearance of the lightning strike.

## V. Scene-Specific Objects (Characters/Props)

These files define complex, composite objects that are specific to the animation being created.

*   **`panda.py`**:
    *   **Purpose**: Defines and constructs a 3D model of a panda. The panda is likely composed of multiple `Sphere` primitives (for the body, head, ears, legs) and uses various shaders (like `PhongShader` and `HemisphereShader`) to give it its characteristic black and white appearance. It also includes a list `tails` for animating the panda's tail.
*   **`cat.py`**:
    *   **Purpose**: Defines and constructs a 3D model of a cat. Similar to the panda, the cat is likely built from `Sphere` primitives for its body parts and potentially `Mesh` objects for more complex parts like ears. It uses `PhongShader` for its material and includes a `tails` list for tail animation.

## VI. Utilities & Configuration

These are helper files and global settings.

*   **`globals.py`**:
    *   **Purpose**: Stores global constants and configuration parameters for the project. This includes image dimensions, animation frame rates, durations, positions for various scene elements (like characters and lightning strike points), and output directory names. Centralizing these values makes them easy to adjust.
*   **`util.py`**:
    *   **Purpose**: Contains general utility functions that might be used across different parts of the project. In this case, it includes a `lerp` function for linear interpolation, which is often useful in animations and graphics.

## VII. Main Application & Orchestration

This is the entry point and main control script for the project.

*   **`main.py`**:
    *   **Purpose**: This is the main script that drives the entire animation and rendering process. It initializes the `RenderWorld`, sets up the camera, lights, and background. It creates and places all the objects in the scene, including the hill, stones, and characters (Panda and Cat). The core logic for the animation sequence (lightning strike, character appearance, tail wagging) is implemented here within a time loop. For each frame of the animation, it updates the scene, renders the image using `world.render()`, converts the pixel data to an image file, and saves it. Finally, it includes a function `show_images()` to display the generated animation frames using `matplotlib`.
