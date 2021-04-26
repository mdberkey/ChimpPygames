import PySimpleGUI as sg
import sys
import os
import subprocess


#sys.path.append(os.path.join("Users", "michaelberkey", "work", "ChimpPygames"))
sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames"))

class Task:
    def __init__(self, name, script_loc, params_loc, results_loc):
        self.name = name
        self.script_loc = script_loc
        self.params_loc = params_loc
        self.results_loc = results_loc

    def get_params(self):
        params = {}
        fileObj = open(self.params_loc, "r")
        for line in fileObj:
            key_value = line.split("=")
            if len(key_value) == 2:
                params[key_value[0].strip()] = key_value[1].strip()
        fileObj.close()
        return params

    def set_params(self, params):
        old_file = open(self.params_loc, "r")
        new_file = open("parameters.dat", "w")

        for line in old_file:
            if line.startswith('#'):
                new_file.write(line)
            else:
                key_value = line.split("=")
                new_file.write(key_value[0] + "= " + params[key_value[0].strip()] + "\n")
        old_file.close()
        new_file.close()
        return True

    def start_task(self):
        try:
            subprocess.call(['sh', "TrainingTaskP1.sh"], cwd="Training_Task")
        except Exception:
            print("Error in opening python script for task: " + self.name)
            print(Exception)


class GUI:
    def __init__(self, size=(500, 300)):
        self.size = size

    def generate_GUI(self):
        tasks = [
            Task("Training 1", "Training_Task/python_scripts/TrainingTaskP1.py", "Training_Task/parametersP1.dat", "Training_Task/resultsP1.csv"),
        ]
        task_names = ["Training 1", "Training 2", "Two Choice Discrimination", "Social Stimuli as Rewards", "Match to Sample", "Delayed Match to Sample", "Oddity Testing", "Delayed Response Task"]
        task_files = ["TrainingTaskP1.sh", "TrainingTaskP2.sh", "TwoChoiceDiscrim.sh", "SocialStimuli.sh", "MathToSample.sh", "DelayedMatchToSample.sh", "OddityTesting.sh", "DelayedResponseTask.sh"]


        task_col = [[sg.Button(task_names[i])] for i in range(len(task_names))]
        option_col = [[sg.Button(tasks[0].name)]]
        print(task_col)
        other_col = []

        #layout = [[sg.Text("Tasks")], [sg.Button("Global Parameters")], task_row_1, task_row_2, task_row_3, task_row_4,
         #         [sg.VSeparator()], [sg.Button("QUIT")]]

        layout = [
            [sg.Column(task_col)],
            [sg.VSeparator()],
            [sg.Column(option_col)],
        ]

        window = sg.Window("Marm Pygames", layout, margins=self.size)
        
        while True:
            event, values = window.read()

            if event == "QUIT" or event == sg.WIN_CLOSED:
                break
            elif event == "Global Parameters":
                pass
            else:
                for task in tasks:
                    if event == task.name:
                        params = task.get_params()
                        print(params)
                        task.set_params(params)
                        task.start_task()

        window.close()

if __name__ == "__main__":
    gui = GUI()
    gui.generate_GUI()
