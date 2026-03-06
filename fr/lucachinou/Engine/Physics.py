import math
import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import Player as Player
import Render as Render
import Render_Shape as Render_Shape

last_time = time.perf_counter()
delta = None

def process_delta():
    global last_time, delta
    now = time.perf_counter()
    delta = now - last_time
    last_time = now

def Apply_Ghost_Platform():
    if Player.Player['PlayerRelative']['FeetPosition'][1] <= 0.0:
        Player.Player['WorldInteraction']['velocity'][1] = 0.0
        Player.Player['PlayerRelative']['on_ground'] = True

def Apply_Velocity():
    Player.Player['PlayerRelative']['FeetPosition'][0] += Player.Player['WorldInteraction']['velocity'][0] * delta
    Player.Player['PlayerRelative']['FeetPosition'][1] += Player.Player['WorldInteraction']['velocity'][1] * delta
    Player.Player['PlayerRelative']['FeetPosition'][2] += Player.Player['WorldInteraction']['velocity'][2] * delta

    vx, vy, vz = Player.Player['WorldInteraction']['velocity']
    speed = math.sqrt(vx * vx + vz * vz)
    if speed > Player.Player['WorldInteraction']['max_walk_speed']:
        factor = Player.Player['WorldInteraction']['max_walk_speed'] / speed
        Player.Player['WorldInteraction']['velocity'][0] *= factor
        Player.Player['WorldInteraction']['velocity'][2] *= factor

def Apply_Gravity():
    if Player.Player['PlayerRelative']['on_ground'] == False:
        Player.Player['WorldInteraction']['velocity'][1] -= Player.Player['WorldInteraction']['gravity'] * delta
    for i in [0, 2]:
        Player.Player['WorldInteraction']['velocity'][i] *= (1 - Player.Player['WorldInteraction']['friction'] * delta)

def Void_death():
    if Player.Player['PlayerRelative']['FeetPosition'][1] <= 0.0:
        Player.Player['PlayerRelative']['FeetPosition'] = [0.0, 1.5, 0.0]

def Apply_Elements_Collisions():
    for element in Render.WorldElements:
        Render_Shape.draw_cube(element['position'][0], element['position'][1], element['position'][2], element['texture'])
        Player.Player['PlayerRelative']['FeetPosition'] = resolve_collision(
            Player.Player['PlayerRelative']['FeetPosition'],
            [0.4, 0.9, 0.4],
            [element['position'][0], element['position'][1], element['position'][2]],
            [(element['size'][0] / 2), (element['size'][1] / 2), (element['size'][2] / 2)]
        )
    Render.DebugElements = [element for element in Render.DebugElements if math.sqrt((Player.Player['PlayerRelative']['FeetPosition'][0] - element[0][0])**2 + (Player.Player['PlayerRelative']['FeetPosition'][1] - element[0][1])**2 + (Player.Player['PlayerRelative']['FeetPosition'][2] - element[0][2])**2) < 3]

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

    if Render.RENDER_FLAGS.get("Debug", False):
        distance = math.sqrt((px - cx)**2 + (py - cy)**2 + (pz - cz)**2)
        if distance < 3:
            Render.DebugElements.append(([cx, cy, cz], [cube_half[0] * 2 + 0.01, cube_half[1] * 2 + 0.01, cube_half[2] * 2 + 0.01]))

    on_ground_per_frame = False

    epsilon = 0.01
    if overlap_x > 0 and overlap_y > 0 and overlap_z > 0:
        overlap_min = min(overlap_x, overlap_y, overlap_z)

        if overlap_min == overlap_y:
            if dy > epsilon and Player.Player['WorldInteraction']['velocity'][1] <= 0:
                py += overlap_y
                on_ground_per_frame = True
                Player.Player['WorldInteraction']['velocity'][1] = 0
            else:
                py -= overlap_y
                on_ground_per_frame = False
        elif overlap_min == overlap_x:
            if (dx > 0 > Player.Player['WorldInteraction']['velocity'][0]) or (dx < 0 < Player.Player['WorldInteraction']['velocity'][0] > 0):
                px += overlap_x * (1 if dx > 0 else -1)
        elif overlap_min == overlap_z:
            if (dz > 0 > Player.Player['WorldInteraction']['velocity'][2]) or (dz < 0 < Player.Player['WorldInteraction']['velocity'][2] > 0):
                pz += overlap_z * (1 if dz > 0 else -1)
    Player.Player['PlayerRelative']['on_ground'] |= on_ground_per_frame
    return [px, py, pz]