import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def dh_transform(theta, d, a, alpha):
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha),  np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta),  np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0,              np.sin(alpha),                 np.cos(alpha),                 d],
        [0,              0,                             0,                             1]
    ])

def forward_kinematics_all_joints(dh_params, base_transform=np.eye(4)):
    T = base_transform.copy()
    positions = [T[:3, 3]]
    for param in dh_params:
        T = T @ dh_transform(*param)
        positions.append(T[:3, 3])
    return np.array(positions)



'''
#Animation for checking fk works
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

line, = ax.plot([], [], [], 'o-', lw=4, color='blue')

def init():
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(0, 3)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    return line,

def update(frame):
    theta1 = np.deg2rad(frame)
    theta2 = np.deg2rad(frame / 2)
    theta3 = np.deg2rad(frame / 3)


    dh_params = [
        (theta1, 0.0, 0.0, np.deg2rad(-90)),
        (theta2, 0.0, 2, 0),
        (theta3, 0.0, 2, 0)
    ]

    base_transform = np.array([
    [np.cos(np.pi/4), -np.sin(np.pi/4), 0, 0],
    [np.sin(np.pi/4),  np.cos(np.pi/4), 0, 0],
    [0,               0,                1, 0.5],
    [0,               0,                0, 1]
    ])

    positions = forward_kinematics_all_joints(dh_params, base_transform)

    line.set_data(positions[:, 0], positions[:, 1])
    line.set_3d_properties(positions[:, 2])
    return line,

ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), init_func=init, blit=False, interval=50)

plt.show()
'''