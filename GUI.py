import PySimpleGUI as sg
import sys
import os
import subprocess

sys.path.append(os.path.join("Users", "michaelberkey", "work", "ChimpPygames"))
#sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames"))

class Task:
    def __init__(self, name, params_loc, results_loc):
        self.name = name
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
        #TODO: get better exception handling
        try:
            subprocess.call(['sh', "TrainingTaskP1.sh"], cwd="Training_Task")
        except Exception:
            print("Error in opening python script for task: " + self.name)


class GUI:
    def __init__(self, size=(500, 300)):
        self.size = size

    def main_menu(self):
        tasks = [
            Task("Training 1", "Training_Task/parametersP1.dat", "Training_Task/resultsP1.csv"),
        ]
        task_names = ["Training 1", "Training 2", "Two Choice Discrimination", "Social Stimuli as Rewards", "Match to Sample", "Delayed Match to Sample", "Oddity Testing", "Delayed Response Task"]
        task_files = ["TrainingTaskP1.sh", "TrainingTaskP2.sh", "TwoChoiceDiscrim.sh", "SocialStimuli.sh", "MathToSample.sh", "DelayedMatchToSample.sh", "OddityTesting.sh", "DelayedResponseTask.sh"]

        task_col = [[sg.Button(tasks[i].name)] for i in range(len(tasks))]
        option_col = [[sg.Button("QUIT")]]

        layout = [
            [sg.Column(task_col)],
            [sg.VSeparator()],
            [sg.Column(option_col)],
        ]

        main_window = sg.Window("Marm Pygames", layout, margins=self.size)
        
        while True:
            event, values = main_window.read()

            if event == "QUIT" or event == sg.WIN_CLOSED:
                break
            elif event == "Global Parameters":
                pass
            else:
                for task in tasks:
                    if event == task.name:
                        self.params_menu(task)
        main_window.close()

    def params_menu(self, task):
        params = task.get_params()
        params_col = []
        for key, value in params.items():
            if value == 'y' or value == 'n':
                params_col.append([sg.Text(key), sg.Checkbox('', key=key)])
            else:
                params_col.append([sg.Text(key), sg.InputText(value, key=key)])

        params_layout = [
            [sg.Column(params_col)],
            [sg.Button("Back to Main Menu"), sg.Button("Confirm Parameters"), sg.Button("Start Task", key='st', visible=True)]
        ]
        params_window = sg.Window(task.name + " Parameters", params_layout, margins=self.size)
        while True:
            event, values = params_window.read()

            if event == "Back to Main Menu" or event == sg.WIN_CLOSED:
                break
            elif event == "Set Parameters":
                for key, value in values.items():
                    if isinstance(value, bool):
                        if value:
                            values[key] = 'y'
                        else:
                            values[key] = 'n'
                task.set_params(values)
                params_window['st'].update("bruh")
                #TODO make start task button appear after parameters have been confirmed!

            elif event == "Start Task":
                task.start_task()

        params_window.close()

if __name__ == "__main__":
    gui = GUI()
    gui.main_menu()
