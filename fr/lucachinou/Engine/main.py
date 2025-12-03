import threading
import time
import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from Player import *
from Input import *
from Render_Shape import *
from Render import *
from RenderUI import *

last_time = time.time()

def resolve_collision(player_pos, player_half, cube_pos, cube_half):
    px, py, pz = player_pos
    cx, cy, cz = cube_pos
    cy += 0.5

    dx = px - cx
    dy = py - cy
    dz = pz - cz

    x_process = (player_half[0] + cube_half[0]) - abs(dx)
    y_process = (player_half[1] + cube_half[1]) - abs(dy)
    z_process = (player_half[2] + cube_half[2]) - abs(dz)

    overlap_x = x_process
    overlap_y = y_process
    overlap_z = z_process

    if RENDER_FLAGS.get("Debug", False):
        DebugElements.append(([cx, cy, cz], [x_process + abs(dx), y_process + abs(dy), z_process + abs(dz)]))

    on_ground_per_frame = False

    epsilon = 0.01
    if overlap_x > 0 and overlap_y > 0 and overlap_z > 0:
        overlap_min = min(overlap_x, overlap_y, overlap_z)

        if overlap_min == overlap_y:
            if dy > 0:
                py += overlap_y
                on_ground_per_frame = True
                Player['WorldInteraction']['velocity'][1] = 0
                print(f"DY: {dy}, on_ground: {on_ground_per_frame}")
            else:
                py -= overlap_y
                on_ground_per_frame = False
        elif overlap_min == overlap_x:
            if RENDER_FLAGS.get("Debug", False):
                print("COLLISION X")
                print(py, cy)
            px += overlap_x * (1 if dx > 0 else -1)
            on_ground_per_frame = False
        elif overlap_min == overlap_z:
            if RENDER_FLAGS.get("Debug", False):
                print("COLLISION Z")
            pz += overlap_z * (1 if dz > 0 else -1)
            on_ground_per_frame = False
    Player['PlayerRelative']['on_ground'] = on_ground_per_frame
    return [px, py, pz]

def display():
    global Player, last_time, DebugElements, RENDER_FLAGS

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    now = time.time()
    dt = now - last_time
    last_time = now

    glRotatef(-Player['CameraRelative']['CameraRotation'][0], -1.0, 0.0, 0.0)
    glRotatef(-Player['CameraRelative']['CameraRotation'][1], 0.0, 1.0, 0.0)
    glTranslatef(-Player['CameraRelative']['CameraPosition'][0], -Player['CameraRelative']['CameraPosition'][1], -Player['CameraRelative']['CameraPosition'][2])

    INPUT_FLAGS.update({"Use_old_placement_mechanics": True, "input_debug": False})
    SHAPE_FLAGS.update({"Load_texture": True})
    RENDER_FLAGS.update({"Debug": False})

    if Player['PlayerRelative']['on_ground'] == False:
        Player['WorldInteraction']['velocity'][1] -= Player['WorldInteraction']['gravity'] * dt * 20

    for i in [0, 2]:
        Player['WorldInteraction']['velocity'][i] *= (1 - Player['WorldInteraction']['friction'] * dt)

    Player['PlayerRelative']['FeetPosition'][0] += Player['WorldInteraction']['velocity'][0] * dt * 20
    Player['PlayerRelative']['FeetPosition'][1] += Player['WorldInteraction']['velocity'][1] * dt * 20
    Player['PlayerRelative']['FeetPosition'][2] += Player['WorldInteraction']['velocity'][2] * dt * 20

    vx, vy, vz = Player['WorldInteraction']['velocity']
    speed = math.sqrt(vx * vx + vz * vz)
    if speed > Player['WorldInteraction']['max_walk_speed']:
        factor = Player['WorldInteraction']['max_walk_speed'] / speed
        Player['WorldInteraction']['velocity'][0] *= factor
        Player['WorldInteraction']['velocity'][2] *= factor

    glEnable(GL_TEXTURE_2D)

    for element in WorldElements:
        draw_cube(element['position'][0], element['position'][1], element['position'][2], element['texture'])
        Player['PlayerRelative']['FeetPosition'] = resolve_collision(
            Player['PlayerRelative']['FeetPosition'],
            [0.2, 0.9, 0.2],
            [element['position'][0], element['position'][1], element['position'][2]],
            [(element['size'][0] / 2), (element['size'][1] / 2), (element['size'][2] / 2)]
        )

    RenderLight()

    if RENDER_FLAGS.get("Debug", False):
        for element in DebugElements:
            draw_wire_cube(
                [element[0][0], element[0][1], element[0][2]],
                [(element[1][0] / 2), (element[1][1] / 2), (element[1][2] / 2)]
            )

    DebugElements = []

    if Player['PlayerRelative']['FeetPosition'][1] <= 0.0:
        Player['WorldInteraction']['velocity'][1] = 0.0
        Player['PlayerRelative']['on_ground'] = True

    keyboard()
    update_camera()

    begin_ortho(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    FeetRound = float(f"{Player['PlayerRelative']['FeetPosition'][0]:.3g}"), float(f"{Player['PlayerRelative']['FeetPosition'][1]:.3g}"), float(f"{Player['PlayerRelative']['FeetPosition'][2]:.3g}")
    draw_text_2d(50, 50, f"X: {FeetRound[0]} / Y: {FeetRound[1]} / Z: {FeetRound[2]}")

    draw_crosshair(*load_texture("crosshair.png"), glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    end_ortho()

    glutSwapBuffers()

def update_camera():
    fx, fy, fz = Player['PlayerRelative']['FeetPosition']
    Player['CameraRelative']['CameraPosition'][0] = fx
    Player['CameraRelative']['CameraPosition'][1] = fy + Player['CameraRelative']['CameraHeight']
    Player['CameraRelative']['CameraPosition'][2] = fz

WorldElements.append({
    'position': [0.0, -1.0, 0.0],
    'size': [1.0, 1.0, 1.0],
    'texture': 'stone.png',
})
WorldElements.append({
    'position': [0.0, 0.0, 2.0],
    'size': [1.0, 1.0, 1.0],
    'texture': 'stone.png',
})

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Engine")
last_mouse_cursor = [glutGet(GLUT_WINDOW_WIDTH)//2, glutGet(GLUT_WINDOW_HEIGHT)//2]
glutPassiveMotionFunc(mouse)
glutDisplayFunc(display)
glutIdleFunc(display)

glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)

glutKeyboardFunc(key_down)
glutKeyboardUpFunc(key_release)

glutSpecialFunc(key_down)
glutSpecialUpFunc(key_release)

glutReshapeFunc(reshape)
glutMouseFunc(mouse_click)
glutSetCursor(GLUT_CURSOR_NONE)
glutMainLoop()