import sys
import os
from random import randint
import pygame as pg
from pygame.locals import *
sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames", "PygameTools"))
import PgTools

# initialize pygame and screen
pg.init()
screen = PgTools.Screen()

file = open("Oddity_Testing/parameters.dat")
params = PgTools.get_params(file)
file.close()

subjectName = str(params["subject_name"])
sampleStimName = str(params["sample_stimulus_name"])
oddStimName = str(params["odd_stimulus_name"])
trialsAmt = int(params["number_of_trials"]) + 1
stimAmt = int(params["number_of_stimuli"])
stimLength = int(params["stimulus_length"])
stimHeight = int(params["stimulus_height"])
passDelay = int(params["passed_inter_trial_interval"])
failDelay = int(params["failed_inter_trial_interval"])
if "y" in str(params["randomly_shaped_stimuli"]) or "Y" in str(params["randomly_shaped_stimuli"]):
    randShapes = True
else:
    randShapes = False


def trial(length, height):
    """
    Initiates a new trial, draws stimuli

    :param length: length of stimuli
    :param height: height of stimuli
    """
    screen.refresh()
    global stimList
    global oddLength
    global oddHeight
    currentLength = int(maxLength / 4)
    currentHeight = int(maxHeight / 4)
    for i in range(stimAmt):
        if i == oddLocation:
            oddLength = currentLength
            oddHeight = currentHeight
            stimList.append(
                pg.draw.rect(
                    screen.fg,
                    PgTools.rand_color(),
                    (currentLength, currentHeight, length, height,),
                )
            )
            PgTools.rand_pattern(
                screen.fg,
                (
                    currentLength,
                    currentHeight,
                ),
                (length, height),
                i=(randint(0, 2), randint(0, 1)),
            )
            if randShapes:
                PgTools.rand_shape(screen.fg, (currentLength, currentHeight),(length, height), oddSeed)
        else:
            stimList.append(
                pg.draw.rect(
                    screen.fg,
                    color,
                    (currentLength, currentHeight, length, height,),
                )
            )
            PgTools.rand_pattern(
                screen.fg,
                (
                    currentLength,
                    currentHeight,
                ),
                (length, height),
                patColor,
                randNums,
            )
            if randShapes:
                PgTools.rand_shape(screen.fg, (currentLength, currentHeight),(length, height), regSeed)
        currentLength += maxLength / 4
        currentLength = int(currentLength)
        if (i + 1) % 3 == 0:
            currentLength = maxLength / 4
            currentLength = int(currentLength)
            currentHeight += maxHeight / 4
            currentHeight= int(currentHeight)

def check_stim(xCoord, yCoord):
    for i in range(stimAmt):
        if i != oddLocation and stimList[i].collidepoint(xCoord, yCoord) and screen.fg.get_at((xCoord, yCoord)) != (0,0,0):
            return True

PgTools.write_ln(
    filename="Oddity_Testing/results.csv",
    data=[
        "subject_name",
        "trial",
        "odd_stim_location",
        "accuracy",
    ],
)

trialNum = 1
colorPair = PgTools.two_rand_color()
patColor = PgTools.rand_color()
randNums = [randint(0, 2), randint(0, 1)]
color = PgTools.rand_color()
patColor = PgTools.rand_color()
oddLocation = randint(0, stimAmt - 1)
stimList = []
maxLength = PgTools.SCREEN_SIZE[0] - stimLength
maxHeight = PgTools.SCREEN_SIZE[1] - stimHeight
oddLength = 0
oddHeight = 0
if randShapes:
    regSeed = randint(0, 99999)
    oddSeed = randint(0, 99999)

trial(stimLength, stimHeight)

# game loop
running = True
while running:
    for event in pg.event.get():
        PgTools.quit_pg(event)
        if event.type == MOUSEBUTTONDOWN:
            xCoord, yCoord = event.pos
            if stimList[oddLocation].collidepoint(xCoord, yCoord) and screen.fg.get_at((xCoord, yCoord)) != (0,0,0):
                PgTools.response(screen, True, passDelay)
                PgTools.write_ln(
                    filename="Oddity_Testing/results.csv",
                    data=[
                        subjectName,
                        trialNum,
                        oddLocation + 1,
                        "passed",
                    ],
                )
            elif check_stim(xCoord, yCoord):
                PgTools.response(screen, False, failDelay)
                PgTools.write_ln(
                    filename="Oddity_Testing/results.csv",
                    data=[
                        subjectName,
                        trialNum,
                        oddLocation + 1,
                        "failed",
                    ],
                )
            else:
                pg.event.clear()
                continue
            trialNum += 1
            if trialNum == trialsAmt:
                PgTools.end_screen(screen)
                while True:
                    for event in pg.event.get():
                        PgTools.quit_pg(event)
            colorPair = PgTools.two_rand_color()
            patColor = PgTools.rand_color()
            randNums = [randint(0, 2), randint(0, 1)]
            color = PgTools.rand_color()
            patColor = PgTools.rand_color()
            oddLocation = randint(0, stimAmt - 1)
            if randShapes:
                regSeed = randint(0, 99999)
                oddSeed = randint(0, 99999)
            trial(stimLength, stimHeight)
    pg.display.update()
