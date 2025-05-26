import numpy as np

OUTPUT_DIR = "out"

IMG_SCALE = 1
IMG_WIDTH = 640
IMG_HEIGHT = 480

POSITIONS = {
    "panda_stone_center": np.array([-2.4, -1.5, 3.0]),
    "panda_center": np.array([-2.1, -1.0, 2.5]),
    "panda_lightning_start": np.array([-5.7, 6.5, 4.1]),
    "panda_lightning_end": np.array([-2.1, -1.5, 3.5]),
    "cat_stone_center": np.array([2.3, -1.5, 3.0]),
    "cat_center": np.array([2, -1.0, 2.5]),
    "cat_lightning_start": np.array([5.7, 6.5, 4.1]),
    "cat_lightning_end": np.array([2, -1.5, 3.5]),
}

ANIMATION_FPS = 12
ANIMATION_DURATION = 36  # animation time for lightning (0 ~ DURATION - 1)
ANIMATION_LIGHTNING_STEPS = 30  # the number of segments of a lightning
ANIMATION_LIGHTNING_DURATION = ANIMATION_DURATION // 3