import os
import json


# GUI
# TASK obj (create, run, read params, export data, set params,)
# engines
# OOP objectives

# list of objects:
# module task scripts (game logic / loop)
# module of static funcs for task scripts (reusable functions)
# data files (output data)
# param files (input data)
# assets / images (stim data)
# device drivers (drivers)
# task class obj
# GUI
# not pure python scripts -> imported by GUI?

def test_func():
    print("Test func")

def read_params(abbr):
    path = os.path.join("data", f"{abbr}_params.json")
    return json.loads(path)
