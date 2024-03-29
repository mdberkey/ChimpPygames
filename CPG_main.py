import PySimpleGUI as sg
import sys
import os
import subprocess
import shutil

#sys.path.append(os.path.join("Users", "michaelberkey", "work", "ChimpPygames"))
sys.path.append(os.path.join("/home", "pi", "Desktop", "ChimpPygames"))


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
        # I know this is bad code, but to fix it would take time which I dont have as of now.
        if self.name == 'Social Stumil as Rewards':
            import Social_Stimuli_As_Rewards.python_scripts.SocialStimuli as ss
            return True
        else:
            subprocess.call(['sh', self.script_file], cwd=self.folder_name)
        return True

    def get_data(self):
        try:
            data_frame = read_csv(self.results_file, sep=',', engine='python', header=None)
            header_list = data_frame.iloc[0].tolist()
            data_list = data_frame[1:].values.tolist()
        except:
            sg.popup_error('Error reading data file.')
            return
        return header_list, data_list


class GUI:
    def __init__(self, size=(500, 300), font="Helvetica 15", header_font="Helvetica 15 underline bold", pad=[5, 5]):
        self.size = size
        self.font = font
        self.header_font = header_font
        self.pad = pad

    def main_menu(self):
        tasks = [
            Task("Training 1", "Training_Task", "TrainingTaskP1.sh", params_file="/parametersP1.dat",
                 results_file="/resultsP1.csv"),
            Task("Training 2", "Training_Task", "TrainingTaskP2.sh", params_file="/parametersP2.dat",
                 results_file="/resultsP2.csv"),
            Task("Two Choice Discrimination", "Two_Choice_Discrimination", "TwoChoiceDiscrim.sh"),
            Task("Social Stimuli as Rewards", "Social_Stimuli_As_Rewards", "SocialStimuli.sh"),
            Task("Match to Sample", "Match_To_Sample", "MatchToSample.sh"),
            Task("Delayed Match to Sample", "Delayed_Match_To_Sample", "DelayedMatchToSample.sh"),
            Task("Oddity Testing", "Oddity_Testing", "OddityTesting.sh"),
            Task("Delayed Response", "Delayed_Response_Task", "DelayedResponseTask.sh"),
            Task("Sides Task", "Sides_Task", "SidesTask.sh")
        ]
        global_params = Task("Global Parameters", "PygameTools", None, params_file="/globalParameters.dat")

        task_col = [[sg.Button(task.name, pad=self.pad)] for task in tasks]
        task_col.insert(0, [sg.Text("Tasks", font=self.header_font)])
        option_col = [
            [sg.Text("Other", font=self.header_font)],
            [sg.Button("Global Parameters", pad=self.pad)],
            [sg.Button("Export Data", pad=self.pad)],
            #[sg.Button("Quick View Data", pad=self.pad)],
            [sg.Button("Delete Data", pad=self.pad)],
            [sg.Button("QUIT", pad=self.pad)]
        ]

        layout = [
            [sg.Column(task_col), sg.VSeparator(), sg.Column(option_col)],
            [sg.Text("For Info/Help: Please refer to the user manual.")],
            [sg.Text("Source Code: https://github.com/mdberkey/ChimpPygames")]
        ]

        main_window = sg.Window("ChimpPygames 0.3.0", layout, margins=self.size, font=self.font)

        while True:
            event, values = main_window.read()

            if event == "QUIT" or event == sg.WIN_CLOSED:
                break
            elif event == "Global Parameters":
                self.params_menu(global_params, is_task=False)
            elif event == "Export Data":
                self.export_data(tasks)
            elif event == "Delete Data":
                self.delete_data(tasks)
            elif event == "Quick View Data":
                self.quick_view_data(tasks)
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
                params_col.append([sg.Text(key, size=(25, 1)), sg.Checkbox('', key=key, default=True)])
            elif value == 'n':
                params_col.append([sg.Text(key, size=(25, 1)), sg.Checkbox('', key=key, default=False)])
            else:
                params_col.append([sg.Text(key, size=(25, 1)), sg.InputText(value, key=key)])

        layout = [
            [sg.Column(params_col)],
            [sg.Button("Back to Main Menu"), sg.Button("Confirm Parameters")],
        ]

        if is_task:
            layout.append([sg.Text("Note: You must \'Confirm Parameters\' before starting task.")])
            start_button = sg.Button("Start Task", disabled=True, key="ST")
            layout[1].append(start_button)

            if task.name == "Social Stimuli as Rewards":
                layout.insert(1, [sg.Button("Open Stimuli", key="SS")])
        else:
            layout.insert(0, [sg.Text("Detected screen Size: " + self.get_screen_size())])
            layout.append([sg.Text("Note: The screen size affects the tasks, not this GUI.")])


        params_window = sg.Window(task.name + " Parameters", layout, margins=self.size, font=self.font)
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
                            if key == "touchscreen_mode":
                                subprocess.Popen(['qjoypad "gamepad"'], shell=True)
                    elif key == "retention_interval_lengths":
                        try:
                            assert(list(map(int, value.split(","))))
                        except ValueError:
                            sg.Popup("Parameter Error: Please separate multiple variables with a ','", font=self.font)
                    elif "name" not in key:
                        try:
                            assert(int(value))
                        except ValueError:
                            sg.Popup("Parameter Error: For the non-naming parameters, please input integer numbers only.", font=self.font)
                task.set_params(values)
                try:
                    start_button.update(disabled=False)
                except UnboundLocalError:
                    pass
            elif event == "ST":
                if task.start_task():
                    sg.Popup("Task Completed.", font=self.font)
            elif event == "SS":
                subprocess.run(["pcmanfm", "/home/pi/Desktop/ChimpPygames/Social_Stimuli_As_Rewards/Social_Stimuli"])

        params_window.close()

    def export_data(self, tasks):
        export_tasks = []
        for task in tasks:
            if os.path.getsize(task.results_file) == 0:
                continue
            else:
                export_tasks.append(task)

        layout = [
            [sg.Text("Task data to be exported:", font=self.header_font, pad=self.pad)]
        ]
        if not export_tasks:
            layout.append([sg.Text("None", pad=self.pad)])
        else:
            for task in export_tasks:
                layout.append([sg.Text(task.name, pad=self.pad)])
        layout.append([sg.Button("Cancel", pad=self.pad), sg.Button("Continue", pad=self.pad)])

        window = sg.Window("Export Data", layout, font=self.font)
        while True:
            event, values = window.read()
            if event == "Cancel" or event == sg.WIN_CLOSED:
                break
            elif event == "Continue":
                for task in export_tasks:
                    shutil.copy(task.results_file, os.path.join("/home", "pi", "Desktop", "CPG Exported Data", task.name + ".csv"))
                sg.Popup("Data Exported to \'~/Desktop/CPG Expored Data\'", font=self.font)
                break
        window.close()

    def delete_data(self, tasks):
        layout = [
            [sg.Text("WARNING", font=self.header_font, pad=self.pad, background_color="red")],
            [sg.Text("This will delete the following non-exported data:", font=self.header_font, pad=self.pad)]
        ]

        for task in tasks:
            if os.path.getsize(task.results_file) == 0:
                continue
            else:
                layout.append([sg.Text(task.name)])
        if len(layout) == 2:
            layout.append([sg.Text("None")])
        layout.append([sg.Button("Cancel", pad=self.pad), sg.Button("Continue", pad=self.pad)])

        window = sg.Window("Delete Data", layout, font=self.font)
        while True:
            event, values = window.read()
            if event == "Cancel" or event == sg.WIN_CLOSED:
                break
            elif event == "Continue":
                for task in tasks:
                    data = open(task.results_file, "w+")
                    data.close()
                sg.Popup("Data Deleted", font=self.font)
                break
        window.close()

    def quick_view_data(self, tasks):
        layout = [
            [sg.Text("Choose data to view:", font=self.header_font, pad=self.pad)],
        ]
        for task in tasks:
            if os.path.getsize(task.results_file) == 0:
                continue
            else:
                layout.append([sg.Button(task.name)])
        if len(layout) == 1:
            layout.append([sg.Text("None")])
        layout.append([sg.Button("Cancel", pad=self.pad)])

        window = sg.Window("Quick View Data", layout, font=self.font)
        while True:
            event, values = window.read()
            if event == "Cancel" or event == sg.WIN_CLOSED:
                break
            else:
                for task in tasks:
                    if event == task.name:
                        headings, data = task.get_data()
                        print(headings, data)
                        data_layout = [
                            [sg.Table(values=data, headings=headings, display_row_numbers=True, num_rows=min(25, len(data)))]
                        ]
                        window = sg.Window(task.name + "Results", data_layout, font=self.font, grab_anywhere=False)
                        while True:
                            event, values = window.read()
                            if event == sg.WIN_CLOSED:
                                break
                        window.close()
        window.close()


    def get_screen_size(self):
        cmd1 = ['xrandr']
        cmd2 = ['grep', '*']
        pipe1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
        pipe2 = subprocess.Popen(cmd2, stdin=pipe1.stdout, stdout=subprocess.PIPE)
        pipe1.stdout.close()
        resolution_string, junk = pipe2.communicate()
        resolution = resolution_string.split()[0]
        return resolution.decode()


if __name__ == "__main__":
    gui = GUI(size=(1, 1))
    gui.main_menu()

