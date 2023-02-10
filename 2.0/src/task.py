import pygame as pg
import json
import taskengines


def create_tasks():
    task_list = []
    for name, abbr in taskengines.names:
        task_list.append(Task(name, abbr))
    return task_list


class Task:

    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr

    def load_params(self):
        # use os.join
        file = open(f"../parameters/{self.abbr}_params.json")
        return json.load(file)
