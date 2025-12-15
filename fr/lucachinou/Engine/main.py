import threading
import time
import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import Player as Player
import Input as Input
import Render_Shape as Render_Shape
import Render as Render
import RenderUI as RenderUI
import Physics as Physics

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(-Player.Player['CameraRelative']['CameraRotation'][0], -1.0, 0.0, 0.0)
    glRotatef(-Player.Player['CameraRelative']['CameraRotation'][1], 0.0, 1.0, 0.0)
    glTranslatef(-Player.Player['CameraRelative']['CameraPosition'][0], -Player.Player['CameraRelative']['CameraPosition'][1], -Player.Player['CameraRelative']['CameraPosition'][2])

    Input.INPUT_FLAGS.update({"Use_old_placement_mechanics": True, "input_debug": False})
    Render_Shape.SHAPE_FLAGS.update({"Load_texture": True})
    Render.RENDER_FLAGS.update({"Debug": False})

    glEnable(GL_TEXTURE_2D)
    Physics.process_delta()

    Physics.Apply_Gravity()
    Physics.Apply_Velocity()

    Player.Player['PlayerRelative']['on_ground'] = False

    Physics.Apply_Elements_Collisions()

    Render.RenderLight()

    Render.Render_Elements_Collisions()

    Physics.Apply_Ghost_Platform()

    Input.keyboard()
    Render.update_camera()

    RenderUI.begin_ortho(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    FeetRound = float(f"{Player.Player['PlayerRelative']['FeetPosition'][0]:.3g}"), float(f"{Player.Player['PlayerRelative']['FeetPosition'][1]:.3g}"), float(f"{Player.Player['PlayerRelative']['FeetPosition'][2]:.3g}")
    RenderUI.draw_text_2d(50, 50, f"X: {FeetRound[0]} / Y: {FeetRound[1]} / Z: {FeetRound[2]}")

    RenderUI.draw_crosshair(*RenderUI.load_texture("crosshair.png"), glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    RenderUI.end_ortho()

    glutSwapBuffers()

Render.WorldElements.append({
    'position': [0.0, -1.0, 0.0],
    'size': [1.0, 1.0, 1.0],
    'texture': 'stone.png',
})
Render.WorldElements.append({
    'position': [0.0, 0.0, 2.0],
    'size': [1.0, 1.0, 1.0],
    'texture': 'stone.png',
})
"""
for x in range(10):
    for z in range(10):
        Render.WorldElements.append({
            'position': [float(x), -1.0, float(z)],
            'size': [1.0, 1.0, 1.0],
            'texture': 'stone.png',
        })
"""
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Engine")
last_mouse_cursor = [glutGet(GLUT_WINDOW_WIDTH)//2, glutGet(GLUT_WINDOW_HEIGHT)//2]
glutPassiveMotionFunc(Input.mouse)
glutDisplayFunc(display)
glutIdleFunc(display)

glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)

glutKeyboardFunc(Input.key_down)
glutKeyboardUpFunc(Input.key_release)

glutSpecialFunc(Input.key_down)
glutSpecialUpFunc(Input.key_release)

glutReshapeFunc(Render.reshape)
glutMouseFunc(Input.mouse_click)
glutSetCursor(GLUT_CURSOR_NONE)
glutMainLoop()