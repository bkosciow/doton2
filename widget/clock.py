from service.widget import Widget
import datetime


class Clock(Widget):
    def __init__(self, font):
        super().__init__()
        self.font = font
        self.work = True
        self.current = {
            'hour': datetime.datetime.now().strftime("%H"),
            'minute': datetime.datetime.now().strftime("%M"),
        }
        self.on_screen = {
            'hour': None,
            'minute': None
        }
        self.colours = {
            'background': (127, 32, 64),
            'digit_background': (0, 0, 0),
            'border': (244, 244, 244)
        }
        self.initialized = False

    def draw_widget(self, lcd, pos_x, pos_y):
        """draw a tile"""
        lcd.background_color = self.colours['background']
        lcd.fill_rect(pos_x, pos_y, pos_x + 105, pos_y + 45)

        lcd.color = self.colours['border']
        lcd.draw_circle(pos_x+49, pos_y+18, 2)
        lcd.draw_circle(pos_x+49, pos_y+28, 2)

        lcd.color = self.colours['border']
        lcd.draw_rect(pos_x, pos_y, pos_x + 105, pos_y + 45)
        self.draw_values(lcd, pos_x, pos_y, True)
        self.initialized = True

    def draw_values(self, lcd, pos_x, pos_y, force=False):
        """draw values"""
        self.current = {
            'hour': datetime.datetime.now().strftime("%H"),
            'minute': datetime.datetime.now().strftime("%M"),
        }
        self.draw_number(
            lcd, pos_x+7, pos_y+8, self.font,
            self.current['hour'], self.on_screen['hour'], 20,
            force
        )
        self.draw_number(
            lcd, pos_x+57, pos_y+8, self.font,
            self.current['minute'], self.on_screen['minute'], 20,
            force
        )
        self.on_screen = self.current.copy()

    def update_values(self, values, name=""):
        pass