import sys
import threading
import time
import math
from pathlib import Path

import numpy as np
from OpenGL.raw.GLU import gluPerspective

import Player as Player
import Input as Input
import Render_Shape as Render_Shape
import Render as Render
import RenderUI as RenderUI
import Physics as Physics

import glfw
from OpenGL.GL import *
import platform

from fr.lucachinou.Engine.RenderUI import BitmapFont
from fr.lucachinou.Engine.Render_Shape import draw_pyramid

if platform.system() == "Darwin" or platform.system() == "Linux":
    print("Cross-comptatible is currently in experimental! Please report any issue you have!")

ASSETS_DIR = Path(__file__).parent / "assets"
if not ASSETS_DIR.exists():
    print("Error: Assets directory not presents in the engine file!")
    sys.exit(404)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    width, height = glfw.get_framebuffer_size(window)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70.0, float(width) / float(height), 0.1, 1000.0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glRotatef(-Player.Player['CameraRelative']['CameraRotation'][0], -1.0, 0.0, 0.0)
    glRotatef(-Player.Player['CameraRelative']['CameraRotation'][1], 0.0, 1.0, 0.0)
    glTranslatef(-Player.Player['CameraRelative']['CameraPosition'][0], -Player.Player['CameraRelative']['CameraPosition'][1], -Player.Player['CameraRelative']['CameraPosition'][2])
    Render.update_camera()

    Physics.process_delta()

    Physics.Apply_Gravity()
    Physics.Apply_Velocity()

    Player.Player['PlayerRelative']['on_ground'] = False

    Physics.Apply_Elements_Collisions()

    Render.RenderLight()

    Render.Render_Elements_Collisions()

    #Physics.Apply_Ghost_Platform() Useless due to the default stone platform

    Input.keyboard()
    Physics.Void_death()

    width, height = glfw.get_framebuffer_size(window)

    RenderUI.begin_ortho(width, height)
    if RenderUI.flags['show_debug_screen']:
        FeetRound = float(f"{Player.Player['PlayerRelative']['FeetPosition'][0]:.3g}"), float(f"{Player.Player['PlayerRelative']['FeetPosition'][1]:.3g}"), float(f"{Player.Player['PlayerRelative']['FeetPosition'][2]:.3g}")
        RenderUI.draw_text_2d(50, 50, f"X: {FeetRound[0]} / Y: {FeetRound[1]} / Z: {FeetRound[2]}", font="default", scale=1.0)

    RenderUI.draw_crosshair(*RenderUI.load_texture(Path(ASSETS_DIR / "crosshair.png")), width, height)
    RenderUI.end_ortho()

    glfw.swap_buffers(window)

for x in range(-10, 10):
    for z in range(-10, 10):
        Render.WorldElements.append({
            'position': [float(x), -1.0, float(z)],
            'size': [1.0, 1.0, 1.0],
            'texture': 'stone',
        })

if not glfw.init():
    raise RuntimeError("Failed to initialize glfw")

def mouse_button_callback(window, button, action, mods):
    x, y = glfw.get_cursor_pos(window)
    Input.mouse_click(button, action,x, y)

def keyboard_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS or action == glfw.REPEAT:
        if glfw.get_key_name(key, scancode):
            Input.key_down(glfw.get_key_name(key, scancode))
        else:
            Input.key_down(key)
    elif action == glfw.RELEASE:
        if glfw.get_key_name(key, scancode):
            Input.key_release(glfw.get_key_name(key, scancode))
        else:
            Input.key_release(key)

def mouse_pos_callback(window, x, y):
    width, height = glfw.get_framebuffer_size(window)
    Input.mouse(window, x, y, height, width)

window = glfw.create_window(800, 600, "Engine", None, None)
Render.window = window
glfw.make_context_current(window)
glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

RenderUI.load_fonts()

Input.INPUT_FLAGS.update({"Use_old_placement_mechanics": True, "input_debug": False})
Render_Shape.SHAPE_FLAGS.update({"Load_texture": True})
RenderUI.flags.update({"enable_text_rendering": True, 'show_debug_screen': True}) # Enabling this will allow engine to display your XYZ coordinate
Render.RENDER_FLAGS.update({"Debug": False})

glfw.set_mouse_button_callback(window, mouse_button_callback)
glfw.set_key_callback(window, keyboard_callback)
glfw.set_cursor_pos_callback(window, mouse_pos_callback)

glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_HIDDEN)

Render_Shape.Load_Texture()
glfw.swap_interval(1)

while not glfw.window_should_close(window):
    glfw.poll_events()
    display()
