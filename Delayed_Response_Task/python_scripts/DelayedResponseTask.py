import sys
import os
import random
import pygame as pg
from pygame.locals import *
sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames", "PygameTools"))
import PgTools

# initialize pygame, screen, and clock
pg.init()
screen = PgTools.Screen()
clock = pg.time.Clock()
pg.time.get_ticks()

file = open("Delayed_Response_Task/parameters.dat")
params = PgTools.get_params(file)
file.close()

subjectName = str(params["subject_name"])
SCSStimName = str(params["spatially_cued_stimulus_name"])
otherStimName = str(params["other_stimuli_name"])
trialsAmt = int(params["number_of_trials"]) + 1
stimAmt = int(params["number_of_stimuli"])
locationsAmt = int(params["number_of_possible_SCS_locations"])
stimLength = int(params["stimulus_length"])
stimHeight = int(params["stimulus_height"])
strLengths = str(params["retention_interval_lengths"]).split(",")
RILengths = [int(strLength) for strLength in strLengths]
passDelay = int(params["passed_inter_trial_interval"])
failDelay = int(params["failed_inter_trial_interval"])
if "y" in str(params["randomly_shaped_stimuli"]) or "Y" in str(params["randomly_shaped_stimuli"]):
    randShapes = True
else:
    randShapes = False

if locationsAmt > stimAmt:
    locationsAmt = stimAmt

def trial_P1(length, height):
    """
    Initiates part 1 of a new trial, draws stimuli

    :param length: length of stimuli
    :param height: height of stimuli
    """
    screen.refresh()
    global stimList
    global trialStart
    global SCSLength
    global SCSHeight
    trialStart = True
    currentLength = int(maxLength / 4)
    currentHeight = int(maxHeight / 4)
    for i in range(stimAmt):
        stimList.append(
            pg.draw.rect(
                screen.fg,
                color,
                (currentLength, currentHeight, length, height,),
            )
        )
        if randShapes:
                PgTools.rand_shape(screen.fg, (currentLength, currentHeight),(length, height), seed)
        if i == SCSLocation:
            SCSLength = currentLength
            SCSHeight = currentHeight
        currentLength += maxLength / 4
        currentLength = int(currentLength)
        if (i + 1) % 3 == 0:
            currentLength = maxLength / 4
            currentLength = int(currentLength)
            currentHeight += maxHeight / 4
            currentHeight= int(currentHeight)
    PgTools.set_cursor(screen, randCorner=True)


def trial_P2():
    """
    Initiates part 2 of a trial, redraws stimuli
    """
    screen.bg.fill(PgTools.BLACK)
    screen.refresh()
    global stimList
    global trialStart
    global SCSLength
    global SCSHeight
    trialStart = True
    currentLength = int(maxLength / 4)
    currentHeight = int(maxHeight / 4)
    for i in range(stimAmt):
        stimList.append(
            pg.draw.rect(
                screen.fg,
                color,
                (currentLength, currentHeight, stimLength, stimHeight,),
            )
        )
        if randShapes:
                PgTools.rand_shape(screen.fg, (currentLength, currentHeight),(stimLength, stimHeight), seed)
        if i == SCSLocation:
            SCSLength = currentLength
            SCSHeight = currentHeight
        currentLength += maxLength / 4
        if (i + 1) % 3 == 0:
            currentLength = maxLength / 4
            currentLength = int(currentLength)
            currentHeight += maxHeight / 4
            currentHeight= int(currentHeight)
    PgTools.set_cursor(screen, randCorner=True)


def check_stim(xCoord, yCoord):
    for i in range(stimAmt):
        if i != SCSLocation and stimList[i].collidepoint(xCoord, yCoord):
            return True


PgTools.write_ln(
    filename="Delayed_Response_Task/results.csv",
    data=[
        "subject_name",
        "number_of_possible_locations",
        "trial",
        SCSStimName,
        "SCS_location",
        "RI",
        "accuracy",
    ],
)

trialNum = 1
color = PgTools.rand_color()
patColor = PgTools.rand_color()
randRI = random.choice(RILengths)
possibleLocations = random.sample(range(stimAmt), locationsAmt)
SCSLocation = random.choice(possibleLocations)
stimList = []
maxLength = PgTools.SCREEN_SIZE[0] - stimLength
maxHeight = PgTools.SCREEN_SIZE[1] - stimHeight
SCSLength = 0
SCSHeight = 0
currentTime = pg.time.get_ticks()
delay = 500
changeTime = currentTime + delay
show = True
blinking = True
seed = random.randint(0, 99999)

trial_P1(stimLength, stimHeight)
on_bg = True

# game loop
running = True
while running:
    for event in pg.event.get():
        PgTools.quit_pg(event)
        if event.type == MOUSEMOTION:
            xCoord, yCoord = event.pos
            if trialStart:
                if stimList[SCSLocation].collidepoint(xCoord, yCoord) and not on_bg:
                    screen.bg.fill(PgTools.BLACK)
                    screen.refresh()
                    pg.event.get()
                    pg.time.delay(randRI)
                    pg.event.clear()
                    blinking = False
                    trial_P2()
                    on_bg = True
                    pg.display.update()
                    trialStart = False
                    continue
            else:
                if stimList[SCSLocation].collidepoint(xCoord, yCoord) and not on_bg:
                    PgTools.response(screen, True, passDelay)
                    on_bg = True
                    PgTools.write_ln(
                        filename="Delayed_Response_Task/results.csv",
                        data=[
                            subjectName,
                            locationsAmt,
                            trialNum,
                            "\"" + str(color) + "\"",
                            SCSLocation + 1,
                            randRI,
                            "passed",
                        ],
                    )
                elif check_stim(xCoord, yCoord) and not on_bg:
                    PgTools.response(screen, False, failDelay)
                    on_bg = True
                    PgTools.write_ln(
                        filename="Delayed_Response_Task/results.csv",
                        data=[
                            subjectName,
                            locationsAmt,
                            trialNum,
                            "\"" + str(color) + "\"",
                            SCSLocation + 1,
                            randRI,
                            "failed",
                        ],
                    )
                else:
                    continue
                trialNum += 1
                if trialNum == trialsAmt:
                    PgTools.end_screen(screen)
                    while True:
                        for event in pg.event.get():
                            PgTools.quit_pg(event)
                color = PgTools.rand_color()
                patColor = PgTools.rand_color()
                randRI = random.choice(RILengths)
                SCSLocation = random.choice(possibleLocations)
                blinking = True
                seed = random.randint(0, 99999)
                trial_P1(stimLength, stimHeight)
                #pg.event.clear()
    currentTime = pg.time.get_ticks()
    if blinking:
        if currentTime >= changeTime:
            changeTime = currentTime + delay
            show = not show
        
        stimList[SCSLocation] = pg.draw.rect(
            screen.bg, PgTools.BLACK, (SCSLength, SCSHeight, stimLength, stimHeight)
            )
        if show:
            stimList[SCSLocation] = pg.draw.rect(
                screen.bg, color, (SCSLength, SCSHeight, stimLength, stimHeight,),
            )
            if randShapes:
                PgTools.rand_shape(screen.bg, (SCSLength, SCSHeight),(stimLength, stimHeight), seed)
    on_bg = PgTools.draw_cursor(screen)
    pg.display.update()
