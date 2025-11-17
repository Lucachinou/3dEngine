import math
import threading
import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

Player = {
    'WorldInteraction': {
        'speed': 0.002,
        'gravity': 0.04,
        'friction': 0.04,
        'jump_strengh': 0.35,
        'velocity': [0.0, 0.0, 0.0],
    },
    'CameraRelative': {
        'CameraPosition': [0.0, 0.0, 0.0],
        'CameraRotation': [0.0, 0.0],
        'CameraHeight': 0.7,
    },
    'PlayerRelative': {
        'Scale': 1.0,
        'FeetPosition': [0.0, 0.0, 0.0],
        'on_ground': True,
    },
    'Settings': {
        'ActiveKeys': set(),
        'sensitivity': 0.2,
        'CurrentScreen': None
    }
}

last_time = time.time()

last_mouse_cursor = [0, 0]
angle = 0.0

WorldElements = []

def key_down(key, x, y):
    Player['Settings']['ActiveKeys'].add(key.decode('utf-8'))

def key_release(key, x, y):
    Player['Settings']['ActiveKeys'].remove(key.decode('utf-8'))

def init():
    glClearColor(0.1, 0.4, 0.9, 0.7)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_LIGHTING)

    lightpos = [1.0, 1.0, -1.0, 1.0]
    lightcolor = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightcolor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightcolor)

    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

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

def draw_cube(x, y, z):
    glBegin(GL_QUADS)

    # rouge (face avant)
    glColor3f(1.0, 0.0, 0.0)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-0.5 + x, 0.0 + y, 0.5 + z)
    glVertex3f(0.5 + x, 0.0 + y, 0.5 + z)
    glVertex3f(0.5 + x, 1.0 + y, 0.5 + z)
    glVertex3f(-0.5 + x, 1.0 + y, 0.5 + z)

    # vert (face arrière)
    glColor3f(0.0, 1.0, 0.0)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-0.5 + x, 0.0 + y, -0.5 + z)
    glVertex3f(-0.5 + x, 1.0 + y, -0.5 + z)
    glVertex3f(0.5 + x, 1.0 + y, -0.5 + z)
    glVertex3f(0.5 + x, 0.0 + y, -0.5 + z)

    # bleu (face gauche)
    glColor3f(0.0, 0.0, 1.0)
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-0.5 + x, 0.0 + y, -0.5 + z)
    glVertex3f(-0.5 + x, 0.0 + y, 0.5 + z)
    glVertex3f(-0.5 + x, 1.0 + y, 0.5 + z)
    glVertex3f(-0.5 + x, 1.0 + y, -0.5 + z)

    # jaune (face droite)
    glColor3f(1.0, 1.0, 0.0)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(0.5 + x, 0.0 + y, -0.5 + z)
    glVertex3f(0.5 + x, 1.0 + y, -0.5 + z)
    glVertex3f(0.5 + x, 1.0 + y, 0.5 + z)
    glVertex3f(0.5 + x, 0.0 + y, 0.5 + z)

    # cyan (face haut)
    glColor3f(0.0, 1.0, 1.0)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-0.5 + x, 1.0 + y, -0.5 + z)
    glVertex3f(0.5 + x, 1.0 + y, -0.5 + z)
    glVertex3f(0.5 + x, 1.0 + y, 0.5 + z)
    glVertex3f(-0.5 + x, 1.0 + y, 0.5 + z)

    # magenta (face bas)
    glColor3f(1.0, 0.0, 1.0)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-0.5 + x, 0.0 + y, -0.5 + z)
    glVertex3f(0.5 + x, 0.0 + y, -0.5 + z)
    glVertex3f(0.5 + x, 0.0 + y, 0.5 + z)
    glVertex3f(-0.5 + x, 0.0 + y, 0.5 + z)

    glEnd()


def draw_pyramid(x, y, z):
    glBegin(GL_TRIANGLES)

    # rouge
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-1.0 + x, -1.0 + y, 1.0 + z)
    glVertex3f(1.0 + x, -1.0 + y, 1.0 + z)
    glVertex3f(0.0 + x, 1.0 + y, 0.0 + z)

    # vert
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0 + x, -1.0 + y, -1.0 + z)
    glVertex3f(0.0 + x, 1.0 + y, 0.0 + z)
    glVertex3f(1.0 + x, -1.0 + y, -1.0 + z)

    # bleu
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0 + x, -1.0 + y, -1.0 + z)
    glVertex3f(-1.0 + x, -1.0 + y, 1.0 + z)
    glVertex3f(0.0 + x, 1.0 + y, 0.0 + z)

    # jaune
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0 + x, -1.0 + y, -1.0 + z)
    glVertex3f(0.0 + x, 1.0 + y, 0.0 + z)
    glVertex3f(1.0 + x, -1.0 + y, 1.0 + z)

    glEnd()

def resolve_collision(player_pos, player_half, cube_pos, cube_half):
    px, py, pz = player_pos
    cx, cy, cz = cube_pos

    dx = px - cx
    dy = py - cy
    dz = pz - cz

    overlap_x = (player_half[0] + cube_half[0]) - abs(dx)
    overlap_y = (player_half[1] + cube_half[1]) - abs(dy) + 1.0
    overlap_z = (player_half[2] + cube_half[2]) - abs(dz)

    if overlap_x > 0 and overlap_y > 0 and overlap_z > 0:
        if dy > 0 and overlap_y < overlap_x and overlap_y < overlap_z:
            # TODO: Use only player_half and cube_half instead of hardcoded threshold
            Player['PlayerRelative']['on_ground'] = True
            Player['WorldInteraction']['velocity'][1] = 0
            py += cube_half[1] + player_half[1] - 1.0
            return [px, py, pz]
        if overlap_x < overlap_y and overlap_x < overlap_z and py <= (cy + 1.0):
            px += overlap_x * (1 if dx > 0 else -1)
        elif overlap_y < overlap_z and py <= (cy + 1.0):
            py += overlap_y * (1 if dy > 0 else -1)
        elif overlap_z < overlap_x and py <= (cy + 1.0):
            pz += overlap_z * (1 if dz > 0 else -1)
        else:
            Player['PlayerRelative']['on_ground'] = False
    return [px, py, pz]

def display():
    global Player, last_time

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    now = time.time()
    dt = now - last_time
    last_time = now

    glRotatef(-Player['CameraRelative']['CameraRotation'][0], -1.0, 0.0, 0.0)
    glRotatef(-Player['CameraRelative']['CameraRotation'][1], 0.0, 1.0, 0.0)
    glTranslatef(-Player['CameraRelative']['CameraPosition'][0], -Player['CameraRelative']['CameraPosition'][1], -Player['CameraRelative']['CameraPosition'][2])

    glRotatef(angle, 1.0, 1.0, 0.0)

    if Player['PlayerRelative']['on_ground'] == False:
        Player['WorldInteraction']['velocity'][1] -= Player['WorldInteraction']['gravity'] * dt * 60

    for i in [0, 2]:
        if Player['WorldInteraction']['velocity'][i] > 0:
            Player['WorldInteraction']['velocity'][i] -= Player['WorldInteraction']['friction'] * dt * 60
            if Player['WorldInteraction']['velocity'][i] < 0:
                Player['WorldInteraction']['velocity'][i] = 0
        elif Player['WorldInteraction']['velocity'][i] < 0:
            Player['WorldInteraction']['velocity'][i] -= Player['WorldInteraction']['friction'] * dt * 60
            if Player['WorldInteraction']['velocity'][i] > 0:
                Player['WorldInteraction']['velocity'][i] = 0

    Player['PlayerRelative']['FeetPosition'][0] += Player['WorldInteraction']['velocity'][0] * dt * 60
    Player['PlayerRelative']['FeetPosition'][1] += Player['WorldInteraction']['velocity'][1] * dt * 60
    Player['PlayerRelative']['FeetPosition'][2] += Player['WorldInteraction']['velocity'][2] * dt * 60

    for element in WorldElements:
        draw_cube(element['position'][0], element['position'][1], element['position'][2])
        Player['PlayerRelative']['FeetPosition'] = resolve_collision(
            Player['PlayerRelative']['FeetPosition'],
            [0.25, 0.5, 0.25],
            [element['position'][0], element['position'][1], element['position'][2]],
            [(element['size'][0] / 2), (element['size'][1] / 2), (element['size'][2] / 2)]
        )

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

def keyboard():
    global Player
    #key = key.decode('utf-8')
    forward = get_camera_forward()
    right = get_camera_right()
    if 's' in Player['Settings']['ActiveKeys']:
        Player['PlayerRelative']['FeetPosition'][0] += forward[0] * Player['WorldInteraction']['speed']
        Player['PlayerRelative']['FeetPosition'][2] += forward[2] * Player['WorldInteraction']['speed']
    if 'z' in Player['Settings']['ActiveKeys']:
        Player['PlayerRelative']['FeetPosition'][0] -= forward[0] * Player['WorldInteraction']['speed']
        Player['PlayerRelative']['FeetPosition'][2] -= forward[2] * Player['WorldInteraction']['speed']
    if 'd' in Player['Settings']['ActiveKeys']:
        Player['PlayerRelative']['FeetPosition'][0] += right[0] * Player['WorldInteraction']['speed']
        Player['PlayerRelative']['FeetPosition'][2] += right[2] * Player['WorldInteraction']['speed']
    if 'q' in Player['Settings']['ActiveKeys']:
        Player['PlayerRelative']['FeetPosition'][0] -= right[0] * Player['WorldInteraction']['speed']
        Player['PlayerRelative']['FeetPosition'][2] -= right[2] * Player['WorldInteraction']['speed']
    if 'v' in Player['Settings']['ActiveKeys']: # TODO: Delete this when all velocity test are finished!
        print("Applying velocity..")
        Player['WorldInteraction']['velocity'][1] += 0.1
    if ' ' in Player['Settings']['ActiveKeys']:
        if Player['PlayerRelative']['on_ground']:
            Player['WorldInteraction']['velocity'][1] = Player['WorldInteraction']['jump_strengh']
            Player['PlayerRelative']['on_ground'] = False

def mouse_click(button, state, x, y):
    forward = get_camera_forward()
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        WorldElements.append({
            'position': [int(Player['CameraRelative']['CameraPosition'][0] - forward[0] * 3), int(Player['CameraRelative']['CameraPosition'][1]  - forward[1] * 3), int(Player['CameraRelative']['CameraPosition'][2] - forward[2] * 3)],
            'size': [1.0, 1.0, 1.0],
        })
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        pass

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