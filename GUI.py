import PySimpleGUI as sg
import sys
import os
import subprocess
import shutil

sys.path.append(os.path.join("Users", "michaelberkey", "work", "ChimpPygames"))
#sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames"))


class Task:
    def __init__(self, name, folder_name, script_file, params_file="/parameters.dat", results_file="/results.csv"):
        self.name = name
        self.folder_name = folder_name
        self.script_file = script_file
        self.params_file = folder_name + params_file
        self.results_file = folder_name + results_file

    def get_params(self):
        params = {}
        fileObj = open(self.params_file, "r")
        for line in fileObj:
            key_value = line.split("=")
            if len(key_value) == 2:
                params[key_value[0].strip()] = key_value[1].strip()
        fileObj.close()
        return params

    def set_params(self, params):
        old_file = open(self.params_file, "r")
        shutil.copy(self.params_file, self.params_file.split("/")[1])
        new_file = open(self.params_file.split("/")[1], "w")
        for line in old_file:
            if line.startswith('#'):
                new_file.write(line)
            else:
                key_value = line.split("=")
                new_file.write(key_value[0] + "= " + params[key_value[0].strip()] + "\n")
        old_file.close()
        new_file.close()
        os.remove(self.params_file)
        shutil.move(self.params_file.split("/")[1], self.params_file)
        return True

    def start_task(self):
        subprocess.call(['sh', self.script_file], cwd=self.folder_name)
        return True


class GUI:
    def __init__(self, size=(500, 300)):
        self.size = size

    def main_menu(self):
        tasks = [
            Task("Training 1", "Training_Task", "Training_TaskP1.sh", params_file="/parametersP1.dat",
                 results_file="/resultsP1.csv"),
            Task("Training 2", "Training_Task", "Training_TaskP2.sh", params_file="/parametersP2.dat",
                 results_file="/resultsP2.csv"),
            Task("Two Choice Discrimination", "Two_Choice_Discrimination", "TwoChoiceDiscrim.sh"),
            Task("Social Stimuli as Rewards", "Social_Stimuli_As_Rewards", "SocialStimuli.sh"),
            Task("Match to Sample", "Match_To_Sample", "MathToSample.sh"),
            Task("Delayed Match to Sample", "Delayed_Match_To_Sample", "PoopDelayedMatchToSample.sh"),
            Task("Oddity Testing", "Oddity_Testing", "OddityTesting.sh"),
            Task("Delayed Response", "Delayed_Response_Task", "DelayedResponseTask.sh")
        ]
        global_params = Task("Global Parameters", "PygameTools", None, params_file="/globalParameters.dat")

        task_col = [[sg.Button(tasks[i].name, pad=[5, 5])] for i in range(len(tasks))]
        option_col = [
            [sg.Button("Global Parameters", pad=[5, 5])],
            [sg.Button("Export Data", pad=[5, 5])],
            [sg.Button("Delete Data", pad=[5, 5])],
            [sg.Button("QUIT", pad=[5, 5])]
        ]

        layout = [
            [sg.Column(task_col), sg.VSeparator(), sg.Column(option_col)]
        ]

        main_window = sg.Window("Marm Pygames", layout, margins=self.size, font="Helvetica 15")
        
        while True:
            event, values = main_window.read()

            if event == "QUIT" or event == sg.WIN_CLOSED:
                break
            elif event == "Global Parameters":
                self.params_menu(global_params, is_task=False)
            elif event == "Export Data":
                pass
                pass
            else:
                for task in tasks:
                    if event == task.name:
                        self.params_menu(task)
        main_window.close()

    def params_menu(self, task, is_task=True):
        params = task.get_params()
        params_col = []
        for key, value in params.items():
            if value == 'y':
                params_col.append([sg.Text(key), sg.Checkbox('', key=key, default=True)])
            elif value == 'n':
                params_col.append([sg.Text(key), sg.Checkbox('', key=key, default=False)])
            else:
                params_col.append([sg.Text(key), sg.InputText(value, key=key)])

        params_layout = [
            [sg.Column(params_col)],
            [sg.Button("Back to Main Menu"), sg.Button("Confirm Parameters")]
        ]
        if is_task:
            params_layout[1].append(sg.Button("Start Task"))

        params_window = sg.Window(task.name + " Parameters", params_layout, margins=self.size, font="Helvetica 15")
        while True:
            event, values = params_window.read()

            if event == "Back to Main Menu" or event == sg.WIN_CLOSED:
                break
            elif event == "Confirm Parameters":
                for key, value in values.items():
                    if isinstance(value, bool):
                        if value:
                            values[key] = 'y'
                        else:
                            values[key] = 'n'
                task.set_params(values)
            elif event == "Start Task":
                task.start_task()

        params_window.close()


if __name__ == "__main__":
    gui = GUI()
    gui.main_menu()
