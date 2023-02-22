import os
import json


class DataTool:

    def __init__(self, abbr):
        self.abbr = abbr
        self.params_path = os.path.join("parameters", f"{self.abbr}_params.json")
        self.results_path = os.path.join("results", f"{self.abbr}_params.json")

    def read_params(self):
        with open(self.params_path, "r") as f:
            return json.load(f)

    def set_params(self, params):
        with open(self.params_path, "w") as f:
            return json.dump(params, f)


def read_glob_params():
    path = os.path.join("parameters", "global_params.json")
    with open(path, "r") as f:
        return json.load(f)
