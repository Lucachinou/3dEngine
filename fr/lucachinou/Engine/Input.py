import math

from OpenGL.GLUT import *

from Player import *
from Render import WorldElements

last_mouse_cursor = [0, 0]
angle = 0.0

def mouse(x, y):
    global last_mouse_cursor

    dx = last_mouse_cursor[0] - x
    dy = y - last_mouse_cursor[1]

    Player['CameraRelative']['CameraRotation'][0] += dy * Player['Settings']['sensitivity']
    Player['CameraRelative']['CameraRotation'][1] += dx * Player['Settings']['sensitivity']

    Player['CameraRelative']['CameraRotation'][0] = max(-89.0, min(89.0, Player['CameraRelative']['CameraRotation'][0]))

    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    glutWarpPointer(width//2, height//2)
    last_mouse_cursor = [width//2, height//2]

    glutPostRedisplay()

def mouse_click(button, state, x, y):
    forward = get_camera_forward()
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        WorldElements.append({
            'position': [int(Player['CameraRelative']['CameraPosition'][0] - forward[0] * 4), int(Player['CameraRelative']['CameraPosition'][1]  - forward[1] * 4), int(Player['CameraRelative']['CameraPosition'][2] - forward[2] * 4)],
            'size': [1.0, 1.0, 1.0],
        })
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        try:
            WorldElements.remove({
                'position': [int(Player['CameraRelative']['CameraPosition'][0] - forward[0] * 4),
                             int(Player['CameraRelative']['CameraPosition'][1] - forward[1] * 4),
                             int(Player['CameraRelative']['CameraPosition'][2] - forward[2] * 4)],
                'size': [1.0, 1.0, 1.0],
            })
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

def key_down(key, x, y):
    Player['Settings']['ActiveKeys'].add(key.decode('utf-8'))

def key_release(key, x, y):
    Player['Settings']['ActiveKeys'].remove(key.decode('utf-8'))

def normalize(v):
    length = math.sqrt(v[0]**2 + v[2]**2)
    if length == 0:
        return v
    return v[0]/length, v[1]/length,v[2]/length

def keyboard():
    global Player
    #key = key.decode('utf-8')
    forward = get_camera_forward()
    forward = normalize((forward[0], 0, forward[2]))

    right = get_camera_right()
    right = normalize((right[0], 0, right[2]))
    if 's' in Player['Settings']['ActiveKeys']:
        if Player['WorldInteraction']['velocity'][0] < Player['WorldInteraction']['max_walk_speed'] and Player['WorldInteraction']['velocity'][2] < Player['WorldInteraction']['max_walk_speed']:
            Player['WorldInteraction']['velocity'][0] += forward[0] * Player['WorldInteraction']['speed']
            Player['WorldInteraction']['velocity'][2] += forward[2] * Player['WorldInteraction']['speed']
    if 'z' in Player['Settings']['ActiveKeys']:
        if Player['WorldInteraction']['velocity'][0] < Player['WorldInteraction']['max_walk_speed'] and Player['WorldInteraction']['velocity'][2] < Player['WorldInteraction']['max_walk_speed']:
            Player['WorldInteraction']['velocity'][0] -= forward[0] * Player['WorldInteraction']['speed']
            Player['WorldInteraction']['velocity'][2] -= forward[2] * Player['WorldInteraction']['speed']
    if 'd' in Player['Settings']['ActiveKeys']:
        if Player['WorldInteraction']['velocity'][0] < Player['WorldInteraction']['max_walk_speed'] and Player['WorldInteraction']['velocity'][2] < Player['WorldInteraction']['max_walk_speed']:
            Player['WorldInteraction']['velocity'][0] += right[0] * Player['WorldInteraction']['speed']
            Player['WorldInteraction']['velocity'][2] += right[2] * Player['WorldInteraction']['speed']
    if 'q' in Player['Settings']['ActiveKeys']:
        if Player['WorldInteraction']['velocity'][0] < Player['WorldInteraction']['max_walk_speed'] and Player['WorldInteraction']['velocity'][2] < Player['WorldInteraction']['max_walk_speed']:
            Player['WorldInteraction']['velocity'][0] -= right[0] * Player['WorldInteraction']['speed']
            Player['WorldInteraction']['velocity'][2] -= right[2] * Player['WorldInteraction']['speed']
    if 'v' in Player['Settings']['ActiveKeys']: # TODO: Delete this when all velocity test are finished!
        print("Applying velocity..")
        Player['WorldInteraction']['velocity'][1] += 0.1
    if ' ' in Player['Settings']['ActiveKeys']:
        if Player['PlayerRelative']['on_ground']:
            Player['WorldInteraction']['velocity'][1] = Player['WorldInteraction']['jump_strengh']
            Player['PlayerRelative']['on_ground'] = False