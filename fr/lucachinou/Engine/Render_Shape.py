from OpenGL.GL import *
from RenderUI import load_texture

from pathlib import Path

import Render

Asset_file = Path(__file__).parent / "Assets"
Textures = {}
SHAPE_FLAGS = {'Load_texture': True}

def Load_Texture():
    for texture in Asset_file.iterdir():
        if texture.is_file():
            Textures[texture.stem] = load_texture(texture)

def is_block_exist(x, y, z) -> bool:
    for element in Render.WorldElements:
        if element['position'][0] == x and element['position'][1] == y and element['position'][2] == z:
            return True
    return False

def draw_cube(x, y, z, tex_id):
    glBindTexture(GL_TEXTURE_2D, Textures[tex_id][0])
    glBegin(GL_QUADS)

    # rouge (face avant)
    if not is_block_exist(x, y, z + 1):
        if not SHAPE_FLAGS.get('Load_texture', False):
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(1.0, 1.0, 1.0)
        glNormal3f(0.0, 0.0, 1.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(-0.5, 0.0, )
        glVertex3f(-0.5 + x, 0.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.5, 0.0)
        glVertex3f(0.5 + x, 0.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.5, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(-0.5, 1.0)
        glVertex3f(-0.5 + x, 1.0 + y, 0.5 + z)

    # vert (face arrière)
    if not is_block_exist(x, y, z - 1):
        if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(0.0, 1.0, 0.0)
        else: glColor3f(1.0, 1.0, 1.0)
        glNormal3f(0.0, 0.0, -1.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(-0.5, 0.0)
        glVertex3f(-0.5 + x, 0.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(-0.5, 1.0)
        glVertex3f(-0.5 + x, 1.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.5, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.5, 0.0)
        glVertex3f(0.5 + x, 0.0 + y, -0.5 + z)

    # bleu (face gauche)
    if not is_block_exist(x - 1, y, z):
        if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(0.0, 0.0, 1.0)
        else: glColor3f(1.0, 1.0, 1.0)
        glNormal3f(-1.0, 0.0, 0.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5 + x, 0.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5 + x, 0.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 1.0)
        glVertex3f(-0.5 + x, 1.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 1.0)
        glVertex3f(-0.5 + x, 1.0 + y, -0.5 + z)

    # jaune (face droite)
    if not is_block_exist(x + 1, y, z):
        if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(1.0, 1.0, 0.0)
        else: glColor3f(1.0, 1.0, 1.0)
        glNormal3f(1.0, 0.0, 0.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5 + x, 0.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5 + x, 0.0 + y, 0.5 + z)

    # cyan (face haut)
    if not is_block_exist(x, y + 1, z):
        if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(0.0, 1.0, 1.0)
        else: glColor3f(1.0, 1.0, 1.0)
        glNormal3f(0.0, 1.0, 0.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5 + x, 1.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5 + x, 1.0 + y, 0.5 + z)

    # magenta (face bas)
    if not is_block_exist(x, y - 1, z):
        if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(1.0, 0.0, 1.0)
        else: glColor3f(1.0, 1.0, 1.0)
        glNormal3f(0.0, -1.0, 0.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5 + x, 0.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5 + x, 0.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5 + x, 0.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5 + x, 0.0 + y, 0.5 + z)

    glEnd()

def outdated_draw_cube(x, y, z, tex_id):
    glBindTexture(GL_TEXTURE_2D, Textures[tex_id][0])
    glBegin(GL_QUADS)

    # rouge (face avant)
    if not is_block_exist(x, y, z + 1):
        if not SHAPE_FLAGS.get('Load_texture', False):
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(1.0, 1.0, 1.0)
        glNormal3f(0.0, 0.0, 1.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(-0.5, 0.0, )
        glVertex3f(-0.5 + x, 0.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.5, 0.0)
        glVertex3f(0.5 + x, 0.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.5, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(-0.5, 1.0)
        glVertex3f(-0.5 + x, 1.0 + y, 0.5 + z)

    # vert (face arrière)
    if not is_block_exist(x, y, z - 1):
        if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(0.0, 1.0, 0.0)
        else: glColor3f(1.0, 1.0, 1.0)
        glNormal3f(0.0, 0.0, -1.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(-0.5, 0.0)
        glVertex3f(-0.5 + x, 0.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(-0.5, 1.0)
        glVertex3f(-0.5 + x, 1.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.5, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.5, 0.0)
        glVertex3f(0.5 + x, 0.0 + y, -0.5 + z)

    # bleu (face gauche)
    if not is_block_exist(x - 1, y, z):
        if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(0.0, 0.0, 1.0)
        else: glColor3f(1.0, 1.0, 1.0)
        glNormal3f(-1.0, 0.0, 0.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5 + x, 0.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5 + x, 0.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 1.0)
        glVertex3f(-0.5 + x, 1.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 1.0)
        glVertex3f(-0.5 + x, 1.0 + y, -0.5 + z)

    # jaune (face droite)
    if not is_block_exist(x + 1, y, z):
        if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(1.0, 1.0, 0.0)
        else: glColor3f(1.0, 1.0, 1.0)
        glNormal3f(1.0, 0.0, 0.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5 + x, 0.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5 + x, 0.0 + y, 0.5 + z)

    # cyan (face haut)
    if not is_block_exist(x, y + 1, z):
        if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(0.0, 1.0, 1.0)
        else: glColor3f(1.0, 1.0, 1.0)
        glNormal3f(0.0, 1.0, 0.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5 + x, 1.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5 + x, 1.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5 + x, 1.0 + y, 0.5 + z)

    # magenta (face bas)
    if not is_block_exist(x, y - 1, z):
        if not SHAPE_FLAGS.get('Load_texture', False): glColor3f(1.0, 0.0, 1.0)
        else: glColor3f(1.0, 1.0, 1.0)
        glNormal3f(0.0, -1.0, 0.0)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5 + x, 0.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5 + x, 0.0 + y, -0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5 + x, 0.0 + y, 0.5 + z)
        if SHAPE_FLAGS.get('Load_texture', False): glTexCoord2f(1.0, 0.0)
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
