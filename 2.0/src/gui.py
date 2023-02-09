import PySimpleGUI as sg
from tasks import tt1

class GUI:

    def __init__(self, size=(500, 300), font="Helvetica 15", header_font="Helvetica 15 underline bold", pad=None):
        self.size = size
        self.font = font
        self.header_font = header_font
        self.pad = pad
        if not pad:
            self.pad = [5, 5]

    def run(self):
        tt1.test()

gui = GUI()
gui.run()

# structure is almost complete.
# need to do some testing to see that
# everything works.
# once that is done, nail GUI / json
# param format.
# then data dump format
# then reimplement methods and tasks
# should be done in about 2 weeks.