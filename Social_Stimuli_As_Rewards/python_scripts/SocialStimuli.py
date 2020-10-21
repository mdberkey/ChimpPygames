import sys
import os
import random
import pygame as pg
from moviepy.editor import *
from pygame.locals import *
sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames", "PygameTools"))
import PgTools

# initialize pygame and screen
pg.init()
screen = PgTools.Screen()

file = open("Social_Stimuli_As_Rewards/parameters.dat")
params = PgTools.get_params(file)
file.close()

subjectName = str(params["subject_name"])
trialsAmt = int(params["number_of_trials"]) + 1
stimRadius = int(params["stimulus_radius"])
stimTime = int(params["stimulus_duration"])


def start_trial(radius):
    """
    Initiates a new trial, draws stimulus
    
    :param radius: radius of stimulus
    """
    screen.refresh()
    global stimulus
    stimulus = pg.draw.circle(
        screen.fg,
        PgTools.GREEN,
        (
            int(PgTools.SCREEN_SIZE[0] / 2),
            int(PgTools.SCREEN_SIZE[1] / 2),
        ),
        radius,
    )


PgTools.write_ln(
    filename="Social_Stimuli_As_Rewards/results.csv",
    data=["subject_name", "trial", "stimulus_size", "image", "image_duration",],
)

path = os.path.join("/home", "pi", "Desktop", "ChimpPygames", "Social_Stimuli_As_Rewards", "Social_Stimuli",)
file = random.choice(os.listdir(path))
if(file.endswith((".mp4", ".mov"))):
    video = VideoFileClip(os.path.join(path, file))
else:
    image = pg.image.load(os.path.join(path, file))


# lags video a lot
# video = video.margin(top=int((PgTools.SCREEN_SIZE[1]-video.h)/2), bottom=int((PgTools.SCREEN_SIZE[1]-video.h)/2), left=int((PgTools.SCREEN_SIZE[0]-video.w)/2), right=int((PgTools.SCREEN_SIZE[0]-video.w)/2))
trialNum = 1
start_trial(stimRadius)

# game loop
running = True
while running:
    for event in pg.event.get():
        PgTools.quit_pg(event)
        if event.type == MOUSEBUTTONDOWN:
            xCoord, yCoord = event.pos
            if stimulus.collidepoint(xCoord, yCoord):
                screen.refresh()
                if(file.endswith((".mp4", ".mov"))):
                    video = VideoFileClip(os.path.join(path, file))
                    # if fullscreen doesnt work for some reason
                    # marginH = int(PgTools.SCREEN_SIZE[1] / 2 - video.h / 2)
                    # marginW = int(PgTools.SCREEN_SIZE[0] / 2 - video.w / 2)
                    # video = video.margin(top=marginH, bottom=marginH, left=marginW, right=marginW)
                    video.preview(fullscreen=True)
                    screen = PgTools.Screen()
                else:
                    image = pg.image.load(os.path.join(path, file))
                    screen.fg.blit(image, (int((PgTools.SCREEN_SIZE[0] - image.get_width()) / 2), int((PgTools.SCREEN_SIZE[1] - image.get_height()) / 2)))
                    pg.display.update()
                    pg.time.delay(stimTime)
                file = random.choice(os.listdir(path))
                pg.event.clear()
                PgTools.write_ln(
                    filename="Social_Stimuli_As_Rewards/results.csv",
                    data=[
                        subjectName,
                        trialNum,
                        int(stimRadius),
                        "foo",
                        stimTime,
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
            start_trial(stimRadius)
    pg.display.update()
