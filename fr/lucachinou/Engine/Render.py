import math

import numpy as np
from OpenGL.GL import *

import Render_Shape
import Player

WorldElements = []
DebugElements = []

window = None

RENDER_FLAGS = {'Debug': False}

def view_matrix(pos, rot):
    pitch = math.radians(rot[0])
    yaw = math.radians(rot[1])

    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)

    Ry = np.array([
        [cy, 0, sy, 0],
        [0, 1, 0, 0],
        [-sy, 0, cy, 0],
        [0, 0, 0, 1],
    ], dtype=np.float32)

    Rx = np.array([
        [1, 0, 0, 0],
        [0, cp, -sp, 0],
        [0, sp, cp, 0],
        [0, 0, 0, 1],
    ], dtype=np.float32)

    T = np.array([
        [1, 0, 0, -pos[0]],
        [0, 1, 0, -pos[1]],
        [0, 0, 1, -pos[2]],
        [0, 0, 0, 1],
    ], dtype=np.float32)

    return Rx @ Ry @ T

def Render_Elements_Collisions():
    if RENDER_FLAGS.get("Debug", False):
        for element in DebugElements:
            Render_Shape.draw_wire_cube(
                [element[0][0], element[0][1], element[0][2]],
                [(element[1][0] / 2), (element[1][1] / 2), (element[1][2] / 2)]
            )

def update_camera():
    fx, fy, fz = Player.Player['PlayerRelative']['FeetPosition']
    Player.Player['CameraRelative']['CameraPosition'][0] = fx
    Player.Player['CameraRelative']['CameraPosition'][1] = fy + Player.Player['CameraRelative']['CameraHeight']
    Player.Player['CameraRelative']['CameraPosition'][2] = fz

def RenderLight():
    glClearColor(0.1, 0.4, 0.9, 0.7)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_LIGHTING)

    lightpos = [0.0, 2.0, 0.0, 1.0]
    lightcolor = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.05, 0.05, 0.05, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightcolor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightcolor)

    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

def perspective(fovy, aspect, znear, zfar):
    f = 1.0 / np.tan(np.radians(fovy) / 2)
    m = np.zeros((4,4), dtype=np.float32)
    m[0,0] = f / aspect
    m[1,1] = f
    m[2,2] = (zfar + znear) / (znear - zfar)
    m[2,3] = (2 * zfar * znear) / (znear - zfar)
    m[3,2] = -1.0
    return m

def reshape(width, height):
    if height == 0:
        height = 1
    aspect = width / height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    obj = perspective(45.0, aspect, 0.1, 50.0)
    glLoadMatrixf(obj.T)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()