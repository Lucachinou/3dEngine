from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


WorldElements = []
DebugElements = []
Debug = True

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