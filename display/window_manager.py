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
                for panel in self.widgets[name]:
                    if not panel.widget.initialized:
                        panel.widget.draw_widget(self.lcd, panel.pos_x, panel.pos_y)
                    panel.widget.draw_values(self.lcd, panel.pos_x, panel.pos_y)


    def stop(self):
        """stops a thread"""
        self.work = False