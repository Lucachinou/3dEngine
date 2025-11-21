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

last_time = time.time()


def resolve_collision(player_pos, player_half, cube_pos, cube_half):
    px, py, pz = player_pos
    cx, cy, cz = cube_pos
    cy += 0.5

    dx = px - cx
    dy = py - cy
    dz = pz - cz

    x_process = (player_half[0] * 2 + cube_half[0]) - abs(dx)
    y_process = (player_half[1] + cube_half[1]) - abs(dy)
    z_process = (player_half[2] * 2 + cube_half[2]) - abs(dz)

    overlap_x = x_process
    overlap_y = y_process
    overlap_z = z_process

    if Debug:
        DebugElements.append(([cx, cy, cz], [x_process + abs(dx), y_process + abs(dy), z_process + abs(dz)]))

    if overlap_x > 0 and overlap_y > 0 and overlap_z > 0:
        if dy > 0 and overlap_y < overlap_x and overlap_y < overlap_z:
            Player['PlayerRelative']['on_ground'] = True
            Player['WorldInteraction']['velocity'][1] = 0
            return [px, py, pz]
        if overlap_x < overlap_y and overlap_x < overlap_z and py <= (cy + 1.0):
            if Debug:
                print("COLLISION X")
            Player['PlayerRelative']['on_ground'] = False
            px += overlap_x * (1 if dx > 0 else -1)
        elif overlap_y < overlap_z and py <= (cy + 1.0):
            if Debug:
                print("COLLISION Y")
            py += overlap_y * (1 if dy > 0 else -1)
        elif overlap_z < overlap_x and py <= (cz + 1.0):
            if Debug:
                print("COLLISION Z")
            Player['PlayerRelative']['on_ground'] = False
            pz += overlap_z * (1 if dz > 0 else -1)
        else:
            Player['PlayerRelative']['on_ground'] = False
    return [px, py, pz]

def display():
    global Player, last_time, DebugElements, Debug

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    now = time.time()
    dt = now - last_time
    last_time = now

    glRotatef(-Player['CameraRelative']['CameraRotation'][0], -1.0, 0.0, 0.0)
    glRotatef(-Player['CameraRelative']['CameraRotation'][1], 0.0, 1.0, 0.0)
    glTranslatef(-Player['CameraRelative']['CameraPosition'][0], -Player['CameraRelative']['CameraPosition'][1], -Player['CameraRelative']['CameraPosition'][2])


    if Player['PlayerRelative']['on_ground'] == False:
        Player['WorldInteraction']['velocity'][1] -= Player['WorldInteraction']['gravity'] * dt * 60

    for i in [0, 2]:
        Player['WorldInteraction']['velocity'][i] *= (1 - Player['WorldInteraction']['friction'] * dt)

    Player['PlayerRelative']['FeetPosition'][0] += Player['WorldInteraction']['velocity'][0] * dt * 60
    Player['PlayerRelative']['FeetPosition'][1] += Player['WorldInteraction']['velocity'][1] * dt * 60
    Player['PlayerRelative']['FeetPosition'][2] += Player['WorldInteraction']['velocity'][2] * dt * 60

    vx, vy, vz = Player['WorldInteraction']['velocity']
    speed = math.sqrt(vx * vx + vz * vz)
    if speed > Player['WorldInteraction']['max_walk_speed']:
        factor = Player['WorldInteraction']['max_walk_speed'] / speed
        Player['WorldInteraction']['velocity'][0] *= factor
        Player['WorldInteraction']['velocity'][2] *= factor

    for element in WorldElements:
        draw_cube(element['position'][0], element['position'][1], element['position'][2])
        Player['PlayerRelative']['FeetPosition'] = resolve_collision(
            Player['PlayerRelative']['FeetPosition'],
            [0.25, 0.5, 0.25],
            [element['position'][0], element['position'][1], element['position'][2]],
            [(element['size'][0] / 2), (element['size'][1] / 2), (element['size'][2] / 2)]
        )
    if Debug:
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

    glutSwapBuffers()

def update_camera():
    fx, fy, fz = Player['PlayerRelative']['FeetPosition']
    Player['CameraRelative']['CameraPosition'][0] = fx
    Player['CameraRelative']['CameraPosition'][1] = fy + Player['CameraRelative']['CameraHeight']
    Player['CameraRelative']['CameraPosition'][2] = fz

def reshape(width, height):
    if height == 0:
        height = 1
    aspect = width / height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, aspect, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

WorldElements.append({
    'position': [0.0, -2.0, 0.0],
    'size': [1.0, 1.0, 1.0],
})
WorldElements.append({
    'position': [0.0, -1.0, 2.0],
    'size': [1.0, 1.0, 1.0],
})

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Engine")
init()
last_mouse_cursor = [glutGet(GLUT_WINDOW_WIDTH)//2, glutGet(GLUT_WINDOW_HEIGHT)//2]
glutPassiveMotionFunc(mouse)
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(key_down)
glutKeyboardUpFunc(key_release)
glutReshapeFunc(reshape)
glutMouseFunc(mouse_click)
glutSetCursor(GLUT_CURSOR_NONE)
glutMainLoop()