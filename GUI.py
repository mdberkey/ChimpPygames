import PySimpleGUI as sg

class GUI:
    def __init__(self, size=(500, 300)):
        self.size = size

    def generate_GUI(self):
        task_names = ["Training 1", "Training 2", "Two Choice Discrimination", "Social Stimuli as Rewards", "Match to Sample", "Delayed Match to Sample", "Oddity Testing", "Delayed Response Task"]
        task_files = ["TrainingTaskP1.sh", "TrainingTaskP2.sh", "TwoChoiceDiscrim.sh", "SocialStimuli.sh", "MathToSample.sh", "DelayedMatchToSample.sh", "OddityTesting.sh", "DelayedResponseTask.sh"]

        task_row_1 = [sg.Button(task_names[0]), sg.Button(task_names[1])]
        task_row_2 = [sg.Button(task_names[2]), sg.Button(task_names[3])]
        task_row_3 = [sg.Button(task_names[4]), sg.Button(task_names[5])]
        task_row_4 = [sg.Button(task_names[6]), sg.Button(task_names[7])]
        task_buttons = [task_row_1, task_row_2, task_row_3, task_row_4]

        layout = [[sg.Text("Tasks")], [sg.Button("Global Parameters")], task_row_1, task_row_2, task_row_3, task_row_4, [sg.Button("QUIT")]]
        window = sg.Window("Marm Pygames", layout, margins=self.size)
        
        while True:
            event, values = window.read()

            if event == "QUIT" or event == sg.WIN_CLOSED:
                break
            elif event == "Global Parameters":
                pass
            else:
                for task in task_names:
                    if event == task:
                        pass 
                        
        window.close()

if __name__ == "__main__":
    gui = GUI()
    gui.generate_GUI()
