import pygame as pg
import json


class Task:
    def __init__(self, disp_name, abbr, in_devices, out_devices):
        self.disp_name = disp_name
        self.abbr = abbr
        self.in_devices = in_devices
        self.out_devices = out_devices

    def load_params(self):
        file = open(f"../parameters/{self.abbr}_params.json")
        return json.load(file)



    # To Do:
    # make task class
    # make other classes
    # clean up code
    # get working with GUI
    # work on new task.