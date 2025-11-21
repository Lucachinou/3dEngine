from OpenGL.GL import *


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

def draw_wire_cube(pos, half):
    x, y, z = pos
    hx, hy, hz = half

    glBegin(GL_LINE_LOOP)
    glVertex3f(x-hx, y-hy, z-hz)
    glVertex3f(x+hx, y-hy, z-hz)
    glVertex3f(x+hx, y+hy, z-hz)
    glVertex3f(x-hx, y+hy, z-hz)
    glEnd()

    glBegin(GL_LINE_LOOP)
    glVertex3f(x-hx, y-hy, z+hz)
    glVertex3f(x+hx, y-hy, z+hz)
    glVertex3f(x+hx, y+hy, z+hz)
    glVertex3f(x-hx, y+hy, z+hz)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(x-hx, y-hy, z-hz); glVertex3f(x-hx, y-hy, z+hz)
    glVertex3f(x+hx, y-hy, z-hz); glVertex3f(x+hx, y-hy, z+hz)
    glVertex3f(x+hx, y+hy, z-hz); glVertex3f(x+hx, y+hy, z+hz)
    glVertex3f(x-hx, y+hy, z-hz); glVertex3f(x-hx, y+hy, z+hz)
    glEnd()
