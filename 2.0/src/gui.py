import PySimpleGUI as sg
import task


class GUI:

    def __init__(self, size=(500, 300), font="Helvetica 15", header_font="Helvetica 15 underline bold", pad=None):
        self.size = size
        self.font = font
        self.header_font = header_font
        self.pad = pad
        if not pad:
            self.pad = (5, 5)
        self.tasks = task.get_tasks()

    def main_menu(self):
        task_column = [[sg.Text("Tasks", font=self.header_font)]]
        for task in self.tasks:
            task_column.append([sg.Button(task.name, pad=self.pad)])
        option_column = [
            [sg.Text("Misc.")]
        ]

        layout = [
            [sg.Column(task_column), sg.VSeparator(), sg.Column(option_column)],
            [sg.Text("For Info/Help: Please refer to the user manual.")],
            [sg.Text("Source Code: https://github.com/mdberkey/ChimpPygames")]
        ]

        main_window = sg.Window("ChimpPygames 1.0.0", layout, margins=self.size, font=self.font)

        while True:
            event, values = main_window.read()

            if event == "QUIT" or event == sg.WIN_CLOSED:
                break
            else:
                for task in self.tasks:
                    if event == task.name:
                        print("hi")
        main_window.close()
