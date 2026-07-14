from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math

WINDOW = 1000

camera_z = 70
time_speed = 1

planet_revolution = [0] * 8
planet_rotation = [0] * 8

# name, orbit_radius, size, rev_speed, rot_speed, color
planets = [
    ("Mercury", 6, 0.4, 4.8, 6, (0.7, 0.7, 0.7)),
    ("Venus", 9, 0.6, 3.5, 4, (0.9, 0.7, 0.2)),
    ("Earth", 13, 0.7, 3, 10, (0.1, 0.4, 1)),
    ("Mars", 17, 0.55, 2.4, 8, (0.9, 0.3, 0.2)),
    ("Jupiter", 23, 1.5, 1.3, 20, (0.9, 0.6, 0.3)),
    ("Saturn", 30, 1.3, 1, 18, (0.9, 0.8, 0.5)),
    ("Uranus", 36, 1.0, 0.7, 15, (0.5, 0.9, 1)),
    ("Neptune", 42, 1.0, 0.5, 14, (0.2, 0.4, 1)),
]

stars = [
    (
        random.uniform(-100, 100),
        random.uniform(-100, 100),
        random.uniform(-100, -10),
    )
    for _ in range(1000)
]


def draw_text(text):
    for c in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))


def draw_orbit(radius):

    glColor3f(0.35, 0.35, 0.35)

    glBegin(GL_LINE_LOOP)

    for i in range(360):

        a = math.radians(i)

        glVertex3f(
            radius * math.cos(a),
            0,
            radius * math.sin(a)
        )

    glEnd()


def draw_stars():

    glPointSize(2)

    glBegin(GL_POINTS)

    for x, y, z in stars:

        glColor3f(1, 1, 1)

        glVertex3f(x, y, z)

    glEnd()


def draw_constellation(points):

    glColor3f(0.6, 0.8, 1)

    glBegin(GL_LINE_STRIP)

    for p in points:
        glVertex3f(*p)

    glEnd()


def draw_constellations():

    orion = [
        (-60, 25, -80),
        (-55, 15, -80),
        (-50, 20, -80),
        (-45, 10, -80),
        (-40, 15, -80),
    ]

    big_dipper = [
        (35, 30, -80),
        (40, 27, -80),
        (45, 25, -80),
        (50, 22, -80),
        (55, 20, -80),
        (60, 25, -80),
        (65, 30, -80)
    ]

    draw_constellation(orion)
    draw_constellation(big_dipper)


def draw_sphere(radius, color):

    glColor3f(*color)

    glutSolidSphere(radius, 40, 40)

def draw_saturn_ring():

    glPushMatrix()

    glRotatef(90, 1, 0, 0)

    glColor3f(0.8, 0.8, 0.6)

    for r in [1.7, 1.9, 2.1]:

        glBegin(GL_LINE_LOOP)

        for i in range(360):

            a = math.radians(i)

            glVertex3f(
                r * math.cos(a),
                r * math.sin(a),
                0
            )

        glEnd()

    glPopMatrix()


def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    gluLookAt(
        0, 20, camera_z,
        0, 0, 0,
        0, 1, 0
    )

    draw_stars()
    draw_constellations()

    # SUN
    glPushMatrix()

    glColor3f(1, 0.8, 0)

    glutSolidSphere(2.5, 60, 60)

    glPopMatrix()

    for i, p in enumerate(planets):

        name, orbit, size, rev, rot, color = p

        draw_orbit(orbit)

        glPushMatrix()

        glRotatef(
            planet_revolution[i],
            0,
            1,
            0
        )

        glTranslatef(orbit, 0, 0)

        glRotatef(
            planet_rotation[i],
            0,
            1,
            0
        )

        draw_sphere(size, color)

        if name == "Saturn":
            draw_saturn_ring()

        glRasterPos3f(
            0,
            size + 1,
            0
        )

        draw_text(name)

        glPopMatrix()

    glutSwapBuffers()


def animate(v):

    for i, p in enumerate(planets):

        planet_revolution[i] += p[3] * 0.2 * time_speed
        planet_rotation[i] += p[4] * time_speed

    glutPostRedisplay()

    glutTimerFunc(16, animate, 0)


def keyboard(key, x, y):

    global camera_z

    if key == b"+":
        camera_z -= 2

    elif key == b"-":
        camera_z += 2


def init():

    glEnable(GL_DEPTH_TEST)

    glClearColor(
        0,
        0,
        0.05,
        1
    )

    glMatrixMode(GL_PROJECTION)

    gluPerspective(
        45,
        1,
        1,
        250
    )

    glMatrixMode(GL_MODELVIEW)


def main():

    glutInit()

    glutInitDisplayMode(
        GLUT_DOUBLE |
        GLUT_RGB |
        GLUT_DEPTH
    )

    glutInitWindowSize(
        WINDOW,
        WINDOW
    )

    glutCreateWindow(
        b"3D Solar System"
    )

    init()

    glutDisplayFunc(display)

    glutKeyboardFunc(keyboard)

    glutTimerFunc(
        16,
        animate,
        0
    )

    glutMainLoop()


main()