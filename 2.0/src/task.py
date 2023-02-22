import json
from taskscripts import tt1, tt2, cht


class Task:

    def __init__(self, name, abbr, script):
        self.name = name
        self.abbr = abbr
        self.run = script


def get_tasks():
    tasks = []
    for name, abbr, script in task_scripts:
        tasks.append(Task(name, abbr, script))
    return tasks


task_scripts = [
    ("Training Task 1", "tt1", tt1.run),
    ("Training Task 2", "tt2", tt2.run),
    ("Chase Task", "cht", cht.run)
]
