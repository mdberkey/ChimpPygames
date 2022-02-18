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

file = open("Sides_Task/parameters.dat")
params = PgTools.get_params(file)
file.close()

subjectName = str(params["subject_name"])
sidesNum = stimAmt = int(params["sides_num"])
consecutiveAmt = int(params["number_of_correct_in_a_row"])
stimWidth = int(params["stimulus_width"])
passDelay = int(params["passed_inter_trial_interval"])
failDelay = int(params["failed_inter_trial_interval"])


def start_trial(width, sideBools):
    """
    Initiates a new trial, draws stimuli

    :param width: width of stimuli
    """
    screen.refresh()

    global stims
    coords = [(0, 0), (0, 0), (PgTools.SCREEN_SIZE[0] - width, 0), (0, PgTools.SCREEN_SIZE[1] - width)]
    sizes = [(PgTools.SCREEN_SIZE[0], width), (width, PgTools.SCREEN_SIZE[1]), (width, PgTools.SCREEN_SIZE[1]), (PgTools.SCREEN_SIZE[0], width)]
    for i in range(4):
        if not sideBools[i]:
            stims[i] = False
            continue

        stims[i] = pg.draw.rect(
            screen.fg,
            PgTools.GREEN,
            (
                coords[i],
                sizes[i],
            ),
        )

    PgTools.set_cursor(screen, mid=True)


def check_stim(xCoord, yCoord):
    for i in range(4):
        if stims[i] and stims[i].collidepoint(xCoord, yCoord):
            global last_stim
            last_stim = i
            return True

PgTools.write_ln(
    filename="Sides_Task/results.csv",
    data=[
        "subject_name",
        "trial",
        "sides_num",
    ],
)

trialNum = 1
sideBools = [False, False, False, False]
last_stim = 0
passedTrials = 0
stims = []
for i in range(sidesNum):
    sideBools[i] = True
start_trial(stimWidth, sideBools)

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
            if check_stim(xCoord, yCoord) and not on_bg:
                PgTools.response(screen, True, passDelay)
                on_bg = True
                PgTools.write_ln(
                    filename="Sides_Task/results.csv",
                    data=[
                        subjectName,
                        trialNum,
                        sidesNum,
                        ],
                )
            else:
                #pg.event.clear()
                continue
            trialNum += 1
            passedTrials += 1
            if passedTrials == consecutiveAmt:
                stims[last_stim] = False
                sideBools[last_stim] = False
                stimAmt -= 1
                passedTrials = 0
            if stimAmt <= 0:
                PgTools.end_screen(screen)
                while True:
                    for event in pg.event.get():
                        PgTools.quit_pg(event)
            start_trial(stimWidth, sideBools)
    on_bg = PgTools.draw_cursor(screen)
    pg.display.update()
