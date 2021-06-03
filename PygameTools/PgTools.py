"""
Provides other programs with useful functionality
"""
import os
import random
import pygame as pg
from pygame.locals import *
from datetime import datetime
import colorsys
import numpy as np

# Reads globalParameters.dat
file = open("PygameTools/globalParameters.dat")
params = {}
for line in file:
    line = line.strip()
    key_value = line.split("=")
    if len(key_value) == 2:
        params[key_value[0].strip()] = key_value[1].strip()
file.close()

# Constants
SCREEN_SIZE = (int(params["screen_width"]), int(params["screen_height"]))  # (length/width, height) of touchscreen in px
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
cursor_visible = True
touchscreen = False
input_mode = MOUSEMOTION
if ("y" in str(params["cursor_hidden"]) or "Y" in str(params["cursor_hidden"])):
    cursor_visible = False
if ("y" in str(params["touchscreen_mode"]) or "Y" in str(params["cursor_hidden"])):
    touchscreen = True
    input_mode = MOUSEBUTTONDOWN


# Screen Tools
class Screen(object):
    def __init__(self, size=SCREEN_SIZE, col=BLACK, fullscreen=True):
        """
        Pygame screen on which to draw stimuli, etc.

        :param size: screen resolution in pixels
        :param col: screen bg color
        :param fullscreen: fullscreen if True, not fullscreen if False
        """
        self.rect = pg.Rect((0, 0), size)
        self.bg = pg.Surface(size)  # static objects go in background (bg)
        self.bg.fill(col)
        flags = pg.FULLSCREEN
        if fullscreen:
            self.fg = pg.display.set_mode(size, flags)  # dynamic objects go in foreground (fg)
        else:
            self.fg = pg.display.set_mode(size)

    def refresh(self):
        """
        Blit background to screen and update display.
        """
        self.fg.blit(self.bg.convert(), (0, 0))
        pg.display.update()


# Game Tools
def get_params(fileObj):
    """
    reads all parameter variables in opened file 'fileObj'
    :return: parameter's values in a dictionary
    """
    if not cursor_visible:  # sets mouse to invisible
        pg.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    global cursor_img
    cursor_img = pg.image.load("reqs/cursor_A.png").convert_alpha()

    params = {}
    for line in fileObj:
        line = line.strip()
        key_value = line.split("=")
        if len(key_value) == 2:
            params[key_value[0].strip()] = key_value[1].strip()
    return params


def quit_pg(event):
    """
    Quit pygame on QUIT, [Esc], and [Q].
    """
    if event.type == QUIT or (event.type == KEYDOWN and (event.key in (K_ESCAPE, K_q))):
        pg.quit()
        raise SystemExit


def response(screen, accuracy=None, delay=5000):
    """
    Game's response to inputs

    :param screen: surface to draw response
    :param accuracy: calls pellet() and sound(correct=True) if True, sound(correct=False) if False
    """
    if accuracy:
        sound(correct=True)
        pellet()
        screen.bg.fill(GREEN)
    elif not accuracy:
        sound(correct=False)
        screen.bg.fill(RED)
    screen.refresh()
    pg.event.get()
    pg.time.delay(delay)
    pg.event.clear()
    screen.bg.fill(BLACK)


def set_cursor(screen, start_x=0, start_y=0, noPos=False, mid=False, randCorner=False):
    """
    sets screen for cursor support
    :param screen: screen obj to set
    :start_x: x coord of cursor start
    :start_y: y coord of cursor start
    """
    if not noPos:
        if mid:
            start_x, start_y = int(SCREEN_SIZE[0] / 2), int(SCREEN_SIZE[1] / 2)
        elif randCorner:
            corner = random.randint(0, 3)
            if corner == 0:
                start_x, start_y = 30, 30
            elif corner == 1:
                start_x, start_y = (SCREEN_SIZE[0] - 30), 30
            elif corner == 2:
                start_x, start_y = 30, (SCREEN_SIZE[1] - 30)
            else:
                start_x, start_y = (SCREEN_SIZE[0] - 30), (SCREEN_SIZE[1] - 30)
        else:
            noPos = True
        pg.mouse.set_pos(start_x, start_y)
    screen.bg.blit(screen.fg.convert(), (0, 0))


def draw_cursor(screen, hidden=touchscreen):
    """
    updates cursor to new position
    :param screen: screen obj to draw cursor upon
    :param hidden: cursor is invisible if False
    :return: True if cursor is on background, false otherwise
    """
    screen.fg.blit(screen.bg.convert(), (0, 0))
    xCoord, yCoord = pg.mouse.get_pos()
    fgColor = screen.fg.get_at((xCoord, yCoord))
    on_bg = False
    if fgColor == (0, 0, 0):
        on_bg = True
    if not hidden:
        screen.fg.blit(cursor_img, (xCoord - 25, yCoord - 25))
    return on_bg


def rand_x_coord(length):
    """
    :param length: length of stimulus
    :return: random x coordinate that fits the stimulus inside the screen
    """
    return random.randint(0, (SCREEN_SIZE[0] - length))


def rand_y_coord(height):
    """
    :param height: height of stimulus
    :return: random y coordinate that fits the stimulus inside the screen
    """
    return random.randint(0, (SCREEN_SIZE[1] - height))


def rand_color(bright=True):
    """
    :param bright: returns only colors that work well on a black background if true
    :return: random rgb color value (x,y,z)
    """
    if bright:
        h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        return tuple([int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)])
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def two_rand_color(bright=True):
    """
    :param bright: returns only colors that work well on a black background if true
    :return: two random rgb color values
    """
    colA = ()
    colB = ()
    if bright:
        h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        colA = tuple([int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)])
        h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        colB = tuple([int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)])
        return colA, colB
    colA = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    colB = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    return colA, colB


def rand_line_point(seed=random.randint(0, 999999), pointA=(0, 0), pointB=(0, 0)):
    """
    Finds a random point between two points on a line.
    :param seed: random seed to be used
    :param pointA: first and lesser point being measured
    :param pointB: Second and greater point being measured
    :return: (x coordinate, y coordinate)
    """
    xCoord = pointA[0]
    yCoord = pointA[1]
    if int(pointA[0]) != int(pointB[0]):
        xCoord = np.random.randint(int(pointA[0]), int(pointB[0]))
    if int(pointA[1]) != int(pointB[1]):
        yCoord = np.random.randint(int(pointA[1]), int(pointB[1]))
    return (xCoord, yCoord)


def rand_shape(screen, coords=(0, 0), size=(0, 0), seed=random.randint(0, 999999), ):
    """
   Draws random black shapes on a rectangular surface to alter the shape of a 
   rectangle to be a random shape
   :param screen: surface pattern is drawn on
    :param coords: (x, y) coordinates of the top-left corner of the pattern square
    :param size: (length, height) size of the pattern square
    :param seed: random seed of the shapes
   """
    np.random.seed(seed)
    randInt = np.random.randint(0, 4)
    if randInt == 0:
        return

    cornerCoords = [coords, (coords[0] + size[0], coords[1]),
                    (coords[0], coords[1] + size[1]), (coords[0] + size[0], coords[1] + size[1]), ]
    midpointCoords = [(int(coords[0] + size[0] / 2), coords[1]), (coords[0], int(coords[1] + size[1] / 2)),
                      (cornerCoords[1][0], int(coords[1] + size[1] / 2)),
                      (int(coords[0] + size[0] / 2), cornerCoords[2][1])]

    if randInt == 1:  # makes the rectangle a triangle in 1 of 4 directions
        i = np.random.randint(0, 4)
        if i == 0:
            pg.draw.polygon(screen, 0, (cornerCoords[0], cornerCoords[1], cornerCoords[2]))
        elif i == 1:
            pg.draw.polygon(screen, 0, (cornerCoords[0], cornerCoords[1], cornerCoords[3]))
        elif i == 2:
            pg.draw.polygon(screen, 0, (cornerCoords[1], cornerCoords[2], cornerCoords[3]))
        else:
            pg.draw.polygon(screen, 0, (cornerCoords[0], cornerCoords[2], cornerCoords[3]))
    elif randInt == 2:  # cuts out a square in 1 of 4 corners
        i = np.random.randint(0, 4)
        if i == 0:
            pg.draw.rect(screen, 0, (cornerCoords[0][0], cornerCoords[0][1],
                                     (midpointCoords[0][0] - cornerCoords[0][0]),
                                     (midpointCoords[1][1] - cornerCoords[0][1])))
        elif i == 1:
            pg.draw.rect(screen, 0, (cornerCoords[2][0], cornerCoords[2][1],
                                     (midpointCoords[3][0] - cornerCoords[2][0]),
                                     (midpointCoords[1][1] - cornerCoords[2][1])))
        elif i == 2:
            pg.draw.rect(screen, 0, (midpointCoords[0][0], midpointCoords[0][1],
                                     (cornerCoords[1][0] - midpointCoords[0][0]),
                                     (midpointCoords[2][1] - cornerCoords[1][1])))
        else:
            pg.draw.rect(screen, 0, (midpointCoords[3][0],
                                     midpointCoords[2][1],
                                     (cornerCoords[3][0] - midpointCoords[3][0]),
                                     (cornerCoords[3][1] - midpointCoords[2][1])))
    elif randInt == 3:  # cuts out randomly sized triangles to make random polygons
        randBool = np.random.randint(0, 2, size=4)
        if bool(randBool[0]):
            pg.draw.polygon(screen, 0, (cornerCoords[0], rand_line_point(seed, cornerCoords[0], midpointCoords[0]),
                                        rand_line_point(seed, cornerCoords[0], midpointCoords[1])))
        if bool(randBool[1]):
            pg.draw.polygon(screen, 0, (cornerCoords[1], rand_line_point(seed, midpointCoords[0], cornerCoords[1]),
                                        rand_line_point(seed, cornerCoords[1], midpointCoords[2])))
        if bool(randBool[2]):
            pg.draw.polygon(screen, 0, (cornerCoords[2], rand_line_point(seed, cornerCoords[2], midpointCoords[3]),
                                        rand_line_point(seed, midpointCoords[1], cornerCoords[2])))
        if bool(randBool[3]):
            pg.draw.polygon(screen, 0, (cornerCoords[3], rand_line_point(seed, midpointCoords[3], cornerCoords[3]),
                                        rand_line_point(seed, midpointCoords[2], cornerCoords[3])))


def rand_pattern(
        screen,
        coords=(0, 0),
        size=(0, 0),
        col=rand_color(),
        i=(random.randint(0, 2), random.randint(0, 1)),
):
    """
    Draws a random pattern in a set area

    :param screen: surface pattern is drawn on
    :param coords: (x, y) coordinates of the top-left corner of the pattern square
    :param size: (length, height) size of the pattern square
    :param col: rgb color of pattern
    :param i: i[0] determines which pattern is chosen, i[1] determines if it is pattern type A or B
    """
    clip = Rect((coords[0], coords[1], size[0], size[1]))
    screen.set_clip(clip)
    if i[0] == 0:
        circle_pat(screen, coords, size, col, i)
    elif i[0] == 1:
        square_pat(screen, coords, size, col, i)
    elif i[0] == 2:
        pass
    screen.set_clip(None)


def circle_pat(screen, coords, size, col, i):
    """
    Draws a circle pattern in a set area

    :param screen: surface pattern is drawn on
    :param coords: (x, y) coordinates of the top-left corner of the pattern square
    :param size: (length, height) size of the pattern square
    :param col: rgb color of pattern
    :param i: i[1] determines if it is pattern type A or B
    """
    xCoord = 0
    yCoord = 0
    radius = 10
    status = True
    rowCount = 0
    for j in range(size[1] + radius):
        if (j - yCoord) == radius:
            for k in range(size[0] + radius):
                if (k - xCoord) == radius and status:
                    pg.draw.circle(screen, col, (coords[0] + k, coords[1] + j), radius)
                    xCoord += radius * 2
                    status = False
                elif (k - xCoord) == radius and not status:
                    xCoord += radius * 2
                    status = True
            if rowCount % 2 == 0:
                status = False
            else:
                status = True
            rowCount += 1
            xCoord = 0
            yCoord += radius * 2
            if i[1] == 0:  # determines if pattern is type A or B
                status = True


def square_pat(screen, coords, size, col, i):
    """
    Draws a square pattern in a set area

    :param screen: surface pattern is drawn on
    :param coords: (x, y) coordinates of the top-left corner of the pattern square
    :param size: (length, height) size of the pattern square
    :param col: rgb color of pattern
    :param i: i[1] determines if it is pattern type A or B
    """
    xCoord = 0
    yCoord = 0
    sideLength = 20
    status = True
    rowCount = 0
    for j in range(size[1] + sideLength):
        if (j - yCoord) == sideLength:
            for k in range(size[0] + sideLength):
                if (k - xCoord) == sideLength and status:
                    pg.draw.rect(
                        screen,
                        col,
                        (coords[0] + k - sideLength, coords[1] + j - sideLength,
                         sideLength, sideLength),
                    )
                    xCoord += sideLength
                    status = False
                elif (k - xCoord) == sideLength and not status:
                    xCoord += sideLength
                    status = True
            if rowCount % 2 == 0:
                status = False
            else:
                status = True
            rowCount += 1
            xCoord = 0
            yCoord += sideLength
            if i[1] == 0:  # determines if pattern is type A or B
                status = True


def pellet(num=1):
    """
        Dispense pellets.

        :param num: number of pellets to dispense
        """
    for i in range(num):
        os.system(
            "sudo python /home/pi/Desktop/ChimpPygames/PygameTools/PelletFeeder/pellet-K1.py"
        )
        print("pellet")


def sound(correct=None):
    """
    Pass True to play whoop (correct.wav); pass False to play buzz (incorrect.wav).

    :param correct: Play one sound if correct is True and another if correct is False
    """
    if correct:
        pg.mixer.Sound(os.path.join("reqs", "sounds", "correct.wav")).play()
        print("correct sound")
    else:
        pg.mixer.Sound(os.path.join("reqs", "sounds", "incorrect.wav")).play()
        print("not correct sound")


def end_screen(screen):
    screen.refresh()
    font = pg.font.SysFont("piday", 50)
    text = font.render('Trials Completed. Press \'esc\' or \'q\' to end task.', True, BLACK, RED).convert()
    screen.fg.blit(text, (75, SCREEN_SIZE[1] / 2))
    pg.display.update()


def write_ln(filename=None, data="", csv=True, date=True):
    """
    Write a list to a file as comma- or tab-delimited. Not passing a list
    results in a blank line. 

    :param filename: filepath to datafile
    :param data: list of data to be output
    :param csv: comma-delimited if True, tab-delimited if False
    :param csv: Adds date/time on each line if True, not if False
    """
    if (date == True):
        data.append(datetime.now().strftime("\"D:%m/%d/%y T:%H:%M:%S\""))
    with open(filename, "a+") as data_file:
        if csv:
            data_file.write(", ".join(map(str, data)) + "\n")
        else:
            data_file.write("\t".join(map(str, data)) + "\n")
