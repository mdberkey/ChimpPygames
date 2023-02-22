from tasktools import data_tool
from tasktools import screen_tool
import pygame as pg


# TODO:
# log hours: (12:00 - 1:30)
# finish basic touch task (easy)
# create simple chase task (medium)
# create list of questions (mediume)
# continue process for rest of tasks (hard)
# get other systems working
# finish

def run():
    pg.init()
    dt = data_tool.DataTool("tt1")
    st = screen_tool.ScreenTool("tt1")
    params = dt.read_params()
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        pg.display.update()
        clock.tick(60)
