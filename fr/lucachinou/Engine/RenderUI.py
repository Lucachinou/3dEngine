from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from pathlib import Path
from PIL import Image

def load_texture(texture_path):
    assets_path = Path(__file__).parent / "assets"
    img = Image.open(assets_path / texture_path)
    img_data = img.convert('RGBA').tobytes()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    return texture, img.width, img.height

def begin_ortho(width, height):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

def end_ortho():
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def draw_text_2d(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    y = glutGet(GLUT_WINDOW_HEIGHT) - y

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT), -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_crosshair(texture, tw, th, screen_width, screen_height):
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBindTexture(GL_TEXTURE_2D, texture)

    x = screen_width / 2.0 - tw / 2.0
    y = screen_height / 2.0 - th / 2.0

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x+tw, y)
    glTexCoord2f(1, 1); glVertex2f(x+tw, y+th)
    glTexCoord2f(0, 1); glVertex2f(x, y+th)
    glEnd()

    glDisable(GL_TEXTURE_2D)