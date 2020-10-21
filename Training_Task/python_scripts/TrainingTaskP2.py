import sys
import os
import pygame as pg
from pygame.locals import *
sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames", "PygameTools"))
import PgTools
import random

# initialize pygame and screen
pg.init()
screen = PgTools.Screen()

file = open("Training_Task/parametersP2.dat")
params = PgTools.get_params(file)
file.close()

subjectName = str(params["subject_name"])
stimLength = int(params["stimulus_length"])
stimHeight = int(params["stimulus_height"])
passDelay = int(params["passed_inter_trial_interval"])
failDelay = int(params["failed_inter_trial_interval"])
if "y" in str(params["randomly_shaped_stimuli"]) or "Y" in str(params["randomly_shaped_stimuli"]):
    randShapes = True
else:
    randShapes = False


def start_trial(length, height):
    """
    Initiates a new trial, draws stimulus

    :param length: length of new stimulus
    :param height: width of new stimulus
    """
    screen.refresh()
    global stimulus
    xCoord = PgTools.rand_x_coord(stimLength)
    yCoord = PgTools.rand_y_coord(stimHeight)
    stimulus = pg.draw.rect(
        screen.fg,
        PgTools.GREEN,
        (xCoord, yCoord, length, height),
    )
    if randShapes:
        PgTools.rand_shape(screen.fg, (xCoord, yCoord), (length, height), randInt)

PgTools.write_ln(
    filename="Training_Task/resultsP2.csv",
    data=["subject_name", "trial", "input_coordinates", "accuracy",],
)

trialNum = 1
passedTrials = 0
randInt = random.randint(0, 99999) # seed
start_trial(stimLength, stimHeight)

# game loop
running = True
while running:
    for event in pg.event.get():
        PgTools.quit_pg(event)
        if event.type == MOUSEBUTTONDOWN:
            xCoord, yCoord = event.pos
            if stimulus.collidepoint(xCoord, yCoord) and screen.fg.get_at((xCoord, yCoord)) != (0,0,0):
                PgTools.response(screen, True, passDelay)
                PgTools.write_ln(
                    filename="Training_Task/resultsP2.csv",
                    data=[subjectName, trialNum, ("\"" + str(xCoord) + ", " + str(yCoord) + "\""), "passed",],
                )
                passedTrials += 1
            else:
                PgTools.response(screen, False, failDelay)
                PgTools.write_ln(
                    filename="Training_Task/resultsP2.csv",
                    data=[subjectName, trialNum, ("\"" + str(xCoord) + ", " + str(yCoord) + "\""), "failed",],
                )
            trialNum += 1
            if passedTrials == 3:
                PgTools.end_screen(screen)
                while True:
                    for event in pg.event.get():
                        PgTools.quit_pg(event)
            start_trial(stimLength, stimHeight)
    pg.display.update()
