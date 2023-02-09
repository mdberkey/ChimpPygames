import pygame as pg
from task import Task

def test():
    print('e')

def creat_task():
    tt1 = Task("Train")

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


# re-blit rects every loop = refresh problem? idk.

# TODO: research and understand pygame more as a refresher
# remake basic image blitting and other things
# remake pygames
# vibe
