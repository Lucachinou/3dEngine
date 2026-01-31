import math
import glfw

from Player import *
from Render import WorldElements
from Render_Shape import is_block_exist
from fr.lucachinou.Engine import RenderUI

last_mouse_cursor = [0, 0]
angle = 0.0

INPUT_FLAGS = {"Use_old_placement_mechanics": True, "input_debug": True}

def mouse(window, x, y, winheight, winwidth):
    global last_mouse_cursor

    dx = last_mouse_cursor[0] - x
    dy = y - last_mouse_cursor[1]

    Player['CameraRelative']['CameraRotation'][0] += dy * Player['Settings']['sensitivity']
    Player['CameraRelative']['CameraRotation'][1] += dx * Player['Settings']['sensitivity']

    Player['CameraRelative']['CameraRotation'][0] = max(-89.0, min(89.0, Player['CameraRelative']['CameraRotation'][0]))

    width = winwidth
    height = winheight
    glfw.set_cursor_pos(window, width // 2, height // 2)
    last_mouse_cursor = [width//2, height//2]

def mouse_click(button, state, x, y):
    if INPUT_FLAGS.get('Use_old_placement_mechanics', False):
        forward = get_camera_forward()
        if button == glfw.MOUSE_BUTTON_1 and state == glfw.PRESS:
            WorldElements.append({
                'position': [int(Player['CameraRelative']['CameraPosition'][0] - forward[0] * 4), int(Player['CameraRelative']['CameraPosition'][1]  - forward[1] * 4), int(Player['CameraRelative']['CameraPosition'][2] - forward[2] * 4)],
                'size': [1.0, 1.0, 1.0],
                'texture': "stone",
            })
        elif button == glfw.MOUSE_BUTTON_2 and state == glfw.PRESS:
            try:
                WorldElements.remove({
                    'position': [int(Player['CameraRelative']['CameraPosition'][0] - forward[0] * 4),
                                 int(Player['CameraRelative']['CameraPosition'][1] - forward[1] * 4),
                                 int(Player['CameraRelative']['CameraPosition'][2] - forward[2] * 4)],
                    'size': [1.0, 1.0, 1.0],
                    'texture': "stone"
                })
            except ValueError:
                pass
    else:
        forward = get_camera_forward()
        px, py, pz = Player['CameraRelative']['CameraPosition']

        target_x = None
        target_y = None
        target_z = None
        for x, y, z in enumerate(forward):
            target_x = px + (1 if -forward[0] > 0 else -1) * math.floor(abs(forward[0]) * x)
            target_y = py + (1 if -forward[1] > 0 else -1) * math.floor(abs(forward[1]) * y)
            target_z = pz + (1 if -forward[2] > 0 else -1) * math.floor(abs(forward[2]) * z)



        block_target = {"position": [int(target_x), int(target_y), int(target_z)], "size": [1.0, 1.0, 1.0], "texture": "stone"}

        if button == glfw.MOUSE_BUTTON_1 and state == glfw.PRESS:
            WorldElements.append(block_target)
        elif button == glfw.MOUSE_BUTTON_2 and state == glfw.PRESS:
            try:
                WorldElements.remove(block_target)
            except ValueError:
                pass

def get_camera_forward():
    yaw = math.radians(Player['CameraRelative']['CameraRotation'][1])
    pitch = math.radians(Player['CameraRelative']['CameraRotation'][0])

    x = math.cos(pitch) * math.sin(yaw)
    y = math.sin(pitch)
    z = math.cos(pitch) * math.cos(yaw)
    return [x, y, z]

def get_camera_right():
    forward = get_camera_forward()
    up = [0, 1, 0]
    right = [
        forward[2]*up[1] - forward[1]*up[2],
        forward[0]*up[2] - forward[2]*up[0],
        forward[1]*up[0] - forward[0]*up[1]
    ]

    length = math.sqrt(right[0]**2 + right[1]**2 + right[2]**2)
    return [right[0]/length, right[1]/length, right[2]/length]

def key_down(key):
    try:Player['Settings']['ActiveKeys'].add(key.decode('utf-8'))
    except KeyError: pass
    except AttributeError: Player['Settings']['ActiveKeys'].add(key)

def key_release(key):
    try:Player['Settings']['ActiveKeys'].remove(key.decode('utf-8'))
    except KeyError: pass
    except AttributeError: Player['Settings']['ActiveKeys'].remove(key)

def normalize(v):
    length = math.sqrt(v[0]**2 + v[2]**2)
    if length == 0:
        return v
    return v[0]/length, v[1]/length,v[2]/length

def keyboard():
    global Player, RENDER_FLAGS
    #key = key.decode('utf-8')
    forward = get_camera_forward()
    forward = normalize((forward[0], 0, forward[2]))

    right = get_camera_right()
    right = normalize((right[0], 0, right[2]))
    if INPUT_FLAGS.get('input_debug', False):
        print("Debugger Player activekey: "+str(Player['Settings']['ActiveKeys']))
        print("Debugger Player activekey: "+str(Player['PlayerRelative']['FeetPosition']))
        print("Debugger Player rotation: "+str(forward)+" Right Direction: "+str(right))
    if 's' in Player['Settings']['ActiveKeys']:
        if Player['WorldInteraction']['velocity'][0] < Player['WorldInteraction']['max_walk_speed'] and Player['WorldInteraction']['velocity'][2] < Player['WorldInteraction']['max_walk_speed']:
            Player['WorldInteraction']['velocity'][0] += forward[0] * Player['WorldInteraction']['speed']
            Player['WorldInteraction']['velocity'][2] += forward[2] * Player['WorldInteraction']['speed']
    if 'z' in Player['Settings']['ActiveKeys']:
        if Player['WorldInteraction']['velocity'][0] < Player['WorldInteraction']['max_walk_speed'] and Player['WorldInteraction']['velocity'][2] < Player['WorldInteraction']['max_walk_speed']:
            Player['WorldInteraction']['velocity'][0] -= forward[0] * Player['WorldInteraction']['speed']
            Player['WorldInteraction']['velocity'][2] -= forward[2] * Player['WorldInteraction']['speed']
    if 'd' in Player['Settings']['ActiveKeys']:
        Player['WorldInteraction']['velocity'][0] += right[0] * Player['WorldInteraction']['speed']
        Player['WorldInteraction']['velocity'][2] += right[2] * Player['WorldInteraction']['speed']
    if 'q' in Player['Settings']['ActiveKeys']:
        Player['WorldInteraction']['velocity'][0] -= right[0] * Player['WorldInteraction']['speed']
        Player['WorldInteraction']['velocity'][2] -= right[2] * Player['WorldInteraction']['speed']
    if '3' in Player['Settings']['ActiveKeys'] and 'H' in Player['Settings']['ActiveKeys']:
        RENDER_FLAGS['Debug'] = True
    if '3' in Player['Settings']['ActiveKeys'] and 'A' in Player['Settings']['ActiveKeys']:
        RENDER_FLAGS['Debug'] = False
    if 32 in Player['Settings']['ActiveKeys']:
        if Player['PlayerRelative']['on_ground']:
            Player['WorldInteraction']['velocity'][1] = Player['WorldInteraction']['jump_strengh']
            Player['PlayerRelative']['on_ground'] = False
    if 292 in Player['Settings']['ActiveKeys']:
        RenderUI.flags['show_debug_screen'] = True
