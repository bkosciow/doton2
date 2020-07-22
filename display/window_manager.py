import threading
from .panel import Panel


class WindowManager(threading.Thread):

    def __init__(self, lcd, touch=None):
        threading.Thread.__init__(self)
        self.work = True
        self.lcd = lcd
        self.widgets = {}
        self.force_draw = True

    def add_widget(self, name, widget, pos_x, pos_y):
        if name not in self.widgets:
            self.widgets[name] = []

        self.widgets[name].append(Panel(widget, pos_x, pos_y))

    def run(self):
        while self.work:
            for name in self.widgets:
                print(name)


    def stop(self):
        """stops a thread"""
        self.work = False