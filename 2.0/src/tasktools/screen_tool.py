import pygame as pg
from tasktools.data_tool import read_glob_params


class ScreenTool:
    def __init__(self, abbr):
        self.abbr = abbr
        gp = read_glob_params()
        self.width = gp["screen_width"]
        self.height = gp["screen_height"]
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(abbr)
