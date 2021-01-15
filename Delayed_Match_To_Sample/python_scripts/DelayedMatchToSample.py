import sys
import os
import random
from random import randint
import pygame as pg
from pygame.locals import *
sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames", "PygameTools"))
import PgTools

# initialize pygame and screen
pg.init()
screen = PgTools.Screen()

file = open("Delayed_Match_To_Sample/parameters.dat")
params = PgTools.get_params(file)
file.close()

subjectName = str(params["subject_name"])
posStimName = str(params["sample/positive_stimulus_name"])
negStimName = str(params["negative_stimulus_name"])
trialsAmt = int(params["number_of_trials"]) + 1
stimAmt = int(params["number_of_comparison_stimuli"])
stimLength = int(params["stimulus_length"])
stimHeight = int(params["stimulus_height"])
strLengths = str(params["retention_interval_lengths"]).split(", ")
RILengths = [int(strLength) for strLength in strLengths]
passDelay = int(params["passed_inter_trial_interval"])
failDelay = int(params["failed_inter_trial_interval"])
if("y" in str(params["sample_stimulus_visible"]) or "Y" in str(params["sample_stimulus_visible"])):
    sampleStimVis = True
else:
    sampleStimVis = False
if "y" in str(params["randomly_shaped_stimuli"]) or "Y" in str(params["randomly_shaped_stimuli"]):
    randShapes = True
else:
    randShapes = False
posLocation = randint(0, stimAmt - 1)

def trial_P1(length, height):
    """
    Initiates part 1 of a new trial, draws sample stimulus

    :param length: length of stimuli
    :param height: height of stimuli
    """
    screen.refresh()
    global trialStart
    global sampleStim
    trialStart = True
    sampleStim = pg.draw.rect(
        screen.fg,
        posColor,
        (
            int((PgTools.SCREEN_SIZE[0] - length) / 2),
            int((PgTools.SCREEN_SIZE[1] - height) / 5),
            length,
            height,
        ),
    )
    PgTools.rand_pattern(
        screen.fg,
        (
            int((PgTools.SCREEN_SIZE[0] - length) * 0.5),
            int((PgTools.SCREEN_SIZE[1] - height) * 0.2),
        ),
        (length, height),
        patColor,
        randNums,
    )
    if randShapes:
        PgTools.rand_shape(screen.fg, ((PgTools.SCREEN_SIZE[0] - length)/2, 
        (PgTools.SCREEN_SIZE[1] - height) / 5), (stimLength, stimHeight), seed)

def trial_P2(posColor):
    """
    Initiates part 2 of a trial, draws comparison stimuli

    :param colorPair: pair of random colors for stimuli base colors
    """
    if not sampleStimVis:
        screen.refresh()

    global stimList
    currentLength = int(maxLength / 4)
    currentHeight = int(maxHeight * 0.4)
    for i in range(stimAmt):
        if i == posLocation:
            stimList.append(
                pg.draw.rect(
                    screen.fg,
                    posColor,
                    (currentLength, currentHeight, stimLength, stimHeight,),
                )
            )
            PgTools.rand_pattern(
            screen.fg, (currentLength, currentHeight), (stimLength, stimHeight), patColor, randNums,
            )
            if randShapes:
                    PgTools.rand_shape(screen.fg, (currentLength, currentHeight),(stimLength, stimHeight), seed)
        else:
            stimList.append(
                pg.draw.rect(
                    screen.fg,
                    PgTools.rand_color(),
                    (currentLength, currentHeight, stimLength, stimHeight,),
                )
            )
            PgTools.rand_pattern(
            screen.fg, (currentLength, currentHeight), (stimLength, stimHeight), PgTools.rand_color(), (randint(0,2), randint(0,2))
            )
            if randShapes:
                PgTools.rand_shape(screen.fg, (currentLength, currentHeight),(stimLength, stimHeight), randint(0, 99999))
        currentLength += maxLength / 2
        currentLength = int(currentLength)
        if i == 1:
            currentLength = int(maxLength / 4)
            currentHeight= int(maxHeight * 0.8)
                posLocation = randint(0, stimAmt)

def check_stim(xCoord, yCoord):
    for i in range(stimAmt):
        if i != posLocation and stimList[i].collidepoint(xCoord, yCoord) and screen.fg.get_at((xCoord, yCoord)) != (0,0,0):
            return True

PgTools.write_ln(
    filename="Match_To_Sample/results.csv",
    data=[
        "subject_name",
        "trial",
        "comparison_stimuli",
        "accuracy",
    ],
)

maxLength = PgTools.SCREEN_SIZE[0] - stimLength
maxHeight = PgTools.SCREEN_SIZE[1] - stimHeight
trialNum = 1
posColor = PgTools.rand_color()
patColor = PgTools.rand_color()
randNums = [randint(0, 2), randint(0, 1)]
stimList = []
seed = random.randint(0, 99999)
randNums = [randint(0, 2), randint(0, 1)]
randRI = random.choice(RILengths)

trial_P1(stimLength, stimHeight)


# game loop
running = True
while running:
    for event in pg.event.get():
        PgTools.quit_pg(event)
        if event.type == MOUSEBUTTONDOWN:
            xCoord, yCoord = event.pos
            if trialStart:
                if sampleStim.collidepoint(xCoord, yCoord) and screen.fg.get_at((xCoord, yCoord)) != (0,0,0):
                    screen.refresh()
                    pg.event.get()
                    pg.time.delay(randRI)
                    pg.event.clear()
                    trial_P2(posColor)
                    pg.display.update()
                    trialStart = False
                    continue
            else:
                posLocation = randint(0, stimAmt)
                if stimList[posLocation].collidepoint(xCoord, yCoord) and screen.fg.get_at((xCoord, yCoord)) != (0,0,0):
                    PgTools.response(screen, True, passDelay)
                    PgTools.write_ln(
                        filename="Match_To_Sample/results.csv",
                        data=[
                            subjectName,
                            trialNum,
                            stimAmt,
                            "passed",
                        ],
                    )
                elif check_stim(xCoord, yCoord):
                    PgTools.response(screen, False, failDelay)
                    PgTools.write_ln(
                        filename="Match_To_Sample/results.csv",
                        data=[
                            subjectName,
                            trialNum,
                            stimAmt,
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
                posColor = PgTools.rand_color()
                patColor = PgTools.rand_color()
                randNums = [randint(0, 2), randint(0, 1)]
                randRI = random.choice(RILengths)
                seed = random.randint(0, 99999)
                trial_P1(stimLength, stimHeight)
                posLocation = randint(0, stimAmt - 1) 
        pg.display.update()
