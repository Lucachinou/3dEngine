import math
import threading
import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

Player = {
    'WorldInteraction': {
        'ActiveKeys': set(),
        'speed': 0.02,
        'gravity': 0.04,
        'jump_strengh': 0.5,
        'velocity': [0.0, 0.0, 0.0],
        'on_ground': False,
    },
    'CameraRelative': {
        'CameraPosition': [0.0, 0.0, 0.0],
        'CameraRotation': [0.0, 0.0],
    },
    'Settings': {
        'sensitivity': 0.2,
        'CurrentScreen': None
    }
}

last_time = time.time()

last_mouse_cursor = [0, 0]
angle = 0.0

WorldElements = []

def key_down(key, x, y):
    Player['WorldInteraction']['ActiveKeys'].add(key.decode('utf-8'))

def key_release(key, x, y):
    Player['WorldInteraction']['ActiveKeys'].remove(key.decode('utf-8'))

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
    global camera_rotiation, last_mouse_cursor

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
    WorldElements.append({'position': [x, y, z], 'size': [1.0, 1.0, 1.0]})
    glBegin(GL_QUADS)

    # rouge
    glColor3f(1.0, 0.0, 0.0)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0 + x, -1.0 + y,  1.0 + z)
    glVertex3f( 1.0 + x, -1.0 + y,  1.0 + z)
    glVertex3f( 1.0 + x,  1.0 + y,  1.0 + z)
    glVertex3f(-1.0 + x,  1.0 + y,  1.0 + z)

    # vert (face arrière)
    glColor3f(0.0, 1.0, 0.0)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-1.0 + x, -1.0 + y, -1.0 + z)
    glVertex3f(-1.0 + x,  1.0 + y, -1.0 + z)
    glVertex3f( 1.0 + x,  1.0 + y, -1.0 + z)
    glVertex3f( 1.0 + x, -1.0 + y, -1.0 + z)

    # bleu (face gauche)
    glColor3f(0.0, 0.0, 1.0)
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-1.0 + x, -1.0 + y, -1.0 + z)
    glVertex3f(-1.0 + x, -1.0 + y,  1.0 + z)
    glVertex3f(-1.0 + x,  1.0 + y,  1.0 + z)
    glVertex3f(-1.0 + x,  1.0 + y, -1.0 + z)

    # jaune (face droite)
    glColor3f(1.0, 1.0, 0.0)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(1.0 + x, -1.0 + y, -1.0 + z)
    glVertex3f(1.0 + x,  1.0 + y, -1.0 + z)
    glVertex3f(1.0 + x,  1.0 + y,  1.0 + z)
    glVertex3f(1.0 + x, -1.0 + y,  1.0 + z)

    # cyan (face haut)
    glColor3f(0.0, 1.0, 1.0)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0 + x,  1.0 + y, -1.0 + z)
    glVertex3f( 1.0 + x,  1.0 + y, -1.0 + z)
    glVertex3f( 1.0 + x,  1.0 + y,  1.0 + z)
    glVertex3f(-1.0 + x,  1.0 + y,  1.0 + z)

    # magenta (face bas)
    glColor3f(1.0, 0.0, 1.0)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-1.0 + x, -1.0 + y, -1.0 + z)
    glVertex3f( 1.0 + x, -1.0 + y, -1.0 + z)
    glVertex3f( 1.0 + x, -1.0 + y,  1.0 + z)
    glVertex3f(-1.0 + x, -1.0 + y,  1.0 + z)

    glEnd()


def draw_pyramid(x, y, z):
    WorldElements.append({'position': [x, y, z], 'size': [1.0, 1.0, 1.0]})
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
    overlap_y = (player_half[1] + cube_half[1]) - abs(dy)
    overlap_z = (player_half[2] + cube_half[2]) - abs(dz)

    if overlap_x > 0 and overlap_y > 0 and overlap_z > 0:
        if overlap_x < overlap_y and overlap_x < overlap_z:
            px += overlap_x * (1 if dx > 0 else -1)
        elif overlap_y < overlap_z:
            py += overlap_y * (1 if dy > 0 else -1)
            Player['WorldInteraction']['on_ground'] = True
        else:
            pz += overlap_z * (1 if dz > 0 else -1)
    return [px, py, pz]

def display():
    global Player, last_time

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    now = time.time()
    dt = now - last_time
    last_time = now
    if Player['WorldInteraction']['on_ground'] == False:
        Player['WorldInteraction']['velocity'][1] -= Player['WorldInteraction']['gravity'] * dt * 60

    Player['CameraRelative']['CameraPosition'][1] += Player['WorldInteraction']['velocity'][1] * dt * 60

    for element in WorldElements:
        Player['CameraRelative']['CameraPosition'] = resolve_collision(
            Player['CameraRelative']['CameraPosition'],
            [0.25, 0.9, 0.25],
            element['position'],
            element['size']
        )

    if Player['CameraRelative']['CameraPosition'][1] <= 0.0:
        Player['CameraRelative']['CameraPosition'][1] = 0.0
        Player['WorldInteraction']['velocity'][1] = 0.0
        Player['WorldInteraction']['on_ground'] = True

    glRotatef(-Player['CameraRelative']['CameraRotation'][0], -1.0, 0.0, 0.0)
    glRotatef(-Player['CameraRelative']['CameraRotation'][1], 0.0, 1.0, 0.0)
    glTranslatef(-Player['CameraRelative']['CameraPosition'][0], -Player['CameraRelative']['CameraPosition'][1], -Player['CameraRelative']['CameraPosition'][2])

    glRotatef(angle, 1.0, 1.0, 0.0)
    draw_cube(0.0, 0.0, 0.0)
    draw_cube(0.0, 0.0, 2.0)
    draw_pyramid(0.0, 0.0, 4.0)

    keyboard()
    glutSwapBuffers()

def keyboard():
    global Player
    #key = key.decode('utf-8')
    forward = get_camera_forward()
    right = get_camera_right()
    if 's' in Player['WorldInteraction']['ActiveKeys']:
        Player['CameraRelative']['CameraPosition'][0] += forward[0] * Player['WorldInteraction']['speed']
        Player['CameraRelative']['CameraPosition'][2] += forward[2] * Player['WorldInteraction']['speed']
    if 'z' in Player['WorldInteraction']['ActiveKeys']:
        Player['CameraRelative']['CameraPosition'][0] -= forward[0] * Player['WorldInteraction']['speed']
        Player['CameraRelative']['CameraPosition'][2] -= forward[2] * Player['WorldInteraction']['speed']
    if 'd' in Player['WorldInteraction']['ActiveKeys']:
        Player['CameraRelative']['CameraPosition'][0] += right[0] * Player['WorldInteraction']['speed']
        Player['CameraRelative']['CameraPosition'][2] += right[2] * Player['WorldInteraction']['speed']
    if 'q' in Player['WorldInteraction']['ActiveKeys']:
        Player['CameraRelative']['CameraPosition'][0] -= right[0] * Player['WorldInteraction']['speed']
        Player['CameraRelative']['CameraPosition'][2] -= right[2] * Player['WorldInteraction']['speed']
    if ' ' in Player['WorldInteraction']['ActiveKeys']:
        if Player['WorldInteraction']['on_ground']:
            Player['WorldInteraction']['velocity'][1] = Player['WorldInteraction']['jump_strengh']
            Player['WorldInteraction']['on_ground'] = False

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
glutSetCursor(GLUT_CURSOR_NONE)
glutMainLoop()