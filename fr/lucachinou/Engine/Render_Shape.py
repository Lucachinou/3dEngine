from OpenGL.GL import *
from RenderUI import load_texture

SHAPE_FLAGS = {'Load_texture': True}

def draw_cube(x, y, z):
    if load_texture("stone.png").get(0):
        glBindTexture(GL_TEXTURE_2D, load_texture("stone.png")[0])
    glBegin(GL_QUADS)

    # rouge (face avant)
    if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(1.0, 0.0, 0.0)
    else: glColor3f(1.0, 1.0, 1.0)
    glNormal3f(0.0, 0.0, 1.0)
    if SHAPE_FLAGS.get('Load_texture', False): glTexCoord3f(-0.5, 0.0, 0.5)
    glVertex3f(-0.5 + x, 0.0 + y, 0.5 + z)
    if SHAPE_FLAGS.get('Load_texture', False): glTexCoord3f(0.5, 0.0, 0.5)
    glVertex3f(0.5 + x, 0.0 + y, 0.5 + z)
    if SHAPE_FLAGS.get('Load_texture', False): glTexCoord3f(0.5, 1.0, 0.5)
    glVertex3f(0.5 + x, 1.0 + y, 0.5 + z)
    if SHAPE_FLAGS.get('Load_texture', False): glTexCoord3f(-0.5, 1.0, 0.5)
    glVertex3f(-0.5 + x, 1.0 + y, 0.5 + z)

    # vert (face arrière)
    if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(0.0, 1.0, 0.0)
    else: glColor3f(1.0, 1.0, 1.0)
    glNormal3f(0.0, 0.0, -1.0)
    if SHAPE_FLAGS.get('Load_texture', False): glTexCoord3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5 + x, 0.0 + y, -0.5 + z)
    if SHAPE_FLAGS.get('Load_texture', False): glTexCoord3f(-0.5, 1.0, -0.5)
    glVertex3f(-0.5 + x, 1.0 + y, -0.5 + z)
    if SHAPE_FLAGS.get('Load_texture', False): glTexCoord3f(0.5, 1.0, -0.5)
    glVertex3f(0.5 + x, 1.0 + y, -0.5 + z)
    if SHAPE_FLAGS.get('Load_texture', False): glTexCoord3f(0.5, 0.0, -0.5)
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
