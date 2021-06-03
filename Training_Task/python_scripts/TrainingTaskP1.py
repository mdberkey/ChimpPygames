import sys
import os
import pygame as pg
from pygame.locals import *
sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames", "PygameTools"))
import PgTools

# initialize pygame and screen
pg.init()
screen = PgTools.Screen()

file = open("Training_Task/parametersP1.dat")
params = PgTools.get_params(file)
file.close()

subjectName = str(params["subject_name"])
trialsAmt = int(params["number_of_trials"]) + 1
stimLength = int(params["first_stimulus_length"])
stimHeight = int(params["first_stimulus_height"])
lastLength = int(params["last_stimulus_length"])
lastHeight = int(params["last_stimulus_height"])
passDelay = int(params["passed_inter_trial_interval"])
failDelay = int(params["failed_inter_trial_interval"])
if "y" in str(params["randomly_shaped_stimuli"]) or "Y" in str(params["randomly_shaped_stimuli"]):
    randShapes = True
else:
    randShapes = False

lengthDecrease = (stimLength - lastLength) / (trialsAmt - 1)
heightDecrease = (stimHeight - lastHeight) / (trialsAmt - 1)

def start_trial(length, height):
    """
    Initiates a new trial, draws stimulus
    :param length: length of new stimulus
    :param height: width of new stimulus
    """
    screen.refresh()

    global stimulus
    x_mid = int((PgTools.SCREEN_SIZE[0] - length) / 2)
    y_mid = int((PgTools.SCREEN_SIZE[1] - height) / 2)

    stimulus = pg.draw.rect(
        screen.fg,
        PgTools.GREEN,
        (
            (x_mid, y_mid),
            (length, height),
        ),
    )
    if randShapes:
        PgTools.rand_shape(screen.fg, (x_mid, y_mid), (length, height))  
    
    PgTools.set_cursor(screen, randCorner=True)


PgTools.write_ln(
    filename="Training_Task/resultsP1.csv",
    data=["subject_name", "trial", "stimulus_size", "input_coordinates", "accuracy",],
)

trialNum = 1
passedTrials = 1
start_trial(stimLength, stimHeight)
on_bg = True

# game loop
running = True
while running:
    for event in pg.event.get():
        PgTools.quit_pg(event)
        if event.type == PgTools.input_mode:
            xCoord, yCoord = event.pos
            if PgTools.touchscreen:
                if screen.fg.get_at((xCoord, yCoord)) != (0, 0, 0):
                    on_bg = False
            if stimulus.collidepoint(xCoord, yCoord) and not on_bg:
                PgTools.response(screen, True, passDelay)
                on_bg = True
                PgTools.write_ln(
                    filename="Training_Task/resultsP1.csv",
                    data=[
                        subjectName,
                        trialNum,
                        "\"" + str((stimLength, stimHeight)) + "\"",
                        "\"" + str((xCoord, yCoord)) + "\"",
                        "passed",
                    ],
                )
                passedTrials += 1
            else:
                continue
            trialNum += 1
            stimLength -= lengthDecrease
            stimHeight -= heightDecrease
            if passedTrials == trialsAmt:
                PgTools.end_screen(screen)
                while True:
                    for event in pg.event.get():
                        PgTools.quit_pg(event)
            start_trial(stimLength, stimHeight)
    
    on_bg = PgTools.draw_cursor(screen)
    pg.display.update()

