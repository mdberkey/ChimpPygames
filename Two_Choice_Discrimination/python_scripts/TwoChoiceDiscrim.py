import sys
import os
import pygame as pg
from pygame.locals import *
sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames", "PygameTools"))
import PgTools
from random import randint


# initialize pygame and screen
pg.init()
screen = PgTools.Screen()

file = open("Two_Choice_Discrimination/parameters.dat")
params = PgTools.get_params(file)
file.close()

subjectName = str(params["subject_name"])
posStimName = str(params["positive_stimulus_name"])
negStimName = str(params["negative_stimulus_name"])
consecutiveAmt = int(params["number_of_correct_in_a_row"])
setsAmt = int(params["number_of_stimulus_pairs"]) + 1
stimLength = int(params["stimulus_length"])
stimHeight = int(params["stimulus_height"])
passDelay = int(params["passed_inter_trial_interval"])
failDelay = int(params["failed_inter_trial_interval"])
if "y" in str(params["randomly_shaped_stimuli"]) or "Y" in str(params["randomly_shaped_stimuli"]):
    randShapes = True
else:
    randShapes = False


def start_trial(length, height, cols):
    """
    Initiates a new trial, draws stimuli

    :param length: length of stimuli
    :param height: height of stimuli
    :param cols: (color1, color2) of stimuli
    """

    screen.refresh()
    while True:
        posX = PgTools.rand_x_coord(length)
        posY = PgTools.rand_y_coord(height)
        negX = PgTools.rand_x_coord(length)
        negY = PgTools.rand_y_coord(height)
        
        global posStim
        global negStim
        posStim = pg.draw.rect(
            screen.fg,
            cols[0],
            (
                posX,
                posY,
                length,
                height,
            ),
        )
        negStim = pg.draw.rect(
            screen.fg,
            cols[1],
            (
                negX,
                negY,
                length,
                height,
            ),
        )
        if posStim.colliderect(negStim):
            screen.refresh()
            continue
        else:
            if randShapes:
                PgTools.rand_shape(screen.fg, (posX, posY,),(length, height), posSeed)
                PgTools.rand_shape(screen.fg, (negX, negY,),(length, height), negSeed)
            break
    PgTools.set_cursor(screen, mid=True)


PgTools.write_ln(
    filename="Two_Choice_Discrimination/results.csv",
    data=[
        "subject_name",
        "set",
        "trial",
        "total_trial",
        posStimName,
        negStimName,
        "input_coordinates",
        "accuracy",
    ],
)

trialNum = 1
setNum = 1
passedTrials = 0
colorPair = PgTools.two_rand_color()
color = PgTools.rand_color()
totalTrial = 1
if randShapes:
    posSeed = randint(0, 99999)
    negSeed = randint(0, 99999)

start_trial(stimLength, stimHeight, colorPair)

# game loop
running = True
while running:
    for event in pg.event.get():
        PgTools.quit_pg(event)
        if event.type == MOUSEMOTION:
            xCoord, yCoord = event.pos
            if posStim.collidepoint(xCoord, yCoord) and screen.fg.get_at((xCoord, yCoord)) != (0,0,0):
                PgTools.response(screen, True, passDelay)
                PgTools.write_ln(
                    filename="Two_Choice_Discrimination/results.csv",
                    data=[
                        subjectName,
                        setNum,
                        trialNum,
                        totalTrial,
                        "\"" + str(colorPair[0]) + "\"",
                        "\"" + str(colorPair[1]) + "\"",
                        "\"" + str((xCoord, yCoord)) + "\"",
                        "passed",
                    ],
                )
                passedTrials += 1
            elif negStim.collidepoint(xCoord, yCoord) and screen.fg.get_at((xCoord, yCoord)) != (0,0,0):
                PgTools.response(screen, False, failDelay)
                PgTools.write_ln(
                    filename="Two_Choice_Discrimination/results.csv",
                    data=[
                        subjectName,
                        setNum,
                        trialNum,
                        totalTrial,
                        "\"" + str(colorPair[0]) + "\"",
                        "\"" + str(colorPair[1]) + "\"",
                        "\"" + str((xCoord, yCoord)) + "\"",
                        "failed",
                    ],
                )
                passedTrials = 0
            else:
                pg.event.clear()
                continue
            trialNum += 1
            totalTrial += 1
            if passedTrials == consecutiveAmt:
                setNum += 1
                colorPair = PgTools.two_rand_color()
                trialNum = 1
                passedTrials = 0
                if randShapes:
                    posSeed = randint(0, 99999)
                    negSeed = randint(0, 99999)
            if setNum == setsAmt:
                PgTools.end_screen(screen)
                while True:
                    for event in pg.event.get():
                        PgTools.quit_pg(event)
            start_trial(stimLength, stimHeight, colorPair)
    PgTools.draw_cursor(screen)
    pg.display.update()
