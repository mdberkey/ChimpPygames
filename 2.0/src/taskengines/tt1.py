import sys
import pygame as pg

import taskengines
from enginetools import tools


def tt1_test():
    tools.tool_test()


def run():
    # setup
    pg.init()
    pg.display.set_caption('')
    clock = pg.time.Clock()

    rect = pg.Surface((50, 50))
    rect.fill('red')

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        pg.display.update()
        clock.tick(60)
