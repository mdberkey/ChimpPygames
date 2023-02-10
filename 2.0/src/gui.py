import PySimpleGUI as sg
import task


class GUI:

    def __init__(self, size=(500, 300), font="Helvetica 15", header_font="Helvetica 15 underline bold", pad=None):
        self.size = size
        self.font = font
        self.header_font = header_font
        self.pad = pad
        if not pad:
            self.pad = [5, 5]

    def run(self):
        tasks = task.create_tasks()
        print(tasks[0].name)

