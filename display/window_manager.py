import threading
from .panel import Panel
from service.widget import Clickable
from PIL import Image
import time


class WindowManager(threading.Thread):

    def __init__(self, lcd, touch=None):
        threading.Thread.__init__(self)
        self.images = {
            "connection_lost": Image.open('assets/image/conn_lost.png')
        }
        self.work = True
        self.lcd = lcd
        self.widgets = {}
        self.force_draw = True
        self.point = None
        self.touch = touch(self.click)
        # self.lcd_used = False

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
                    self._handle_touch()

    def stop(self):
        """stops a thread"""
        self.work = False

    def click(self, point):
        """store touch point"""
        self.point = point
        print(point)

    def _handle_touch(self):
        point = self.point
        self.point = None
        if point is None:
            return

        print("parsing touch")
        for widgets in self.widgets:
            for panel in self.widgets[widgets]:
                if isinstance(panel.widget, Clickable) and \
                        panel.pos_x < point[0] < panel.pos_x + panel.widget.width and \
                        panel.pos_y < point[1] < panel.pos_y + panel.widget.height:
                    panel.widget.action(widgets, point[0] - panel.pos_x, point[1] - panel.pos_y)

    def crash(self):
        self.stop()
        self.widgets = {}
        time.sleep(5)
        self.lcd.transparency_color = (0, 0, 0)
        self.lcd.draw_image(90, 100, self.images['connection_lost'])
