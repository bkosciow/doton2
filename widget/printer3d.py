from service.widget import Widget, Clickable
from PIL import Image
import re
import datetime
import math
import service.comm as comm


class Printer3d(Widget, Clickable):

    def __init__(self, font, light_pin=None, power_pin=None, reverse_relay=True):
        super().__init__()
        self.font = font
        self.work = True
        self.light_pin = light_pin
        self.power_pin = power_pin
        self.reverse_relay = reverse_relay
        self.reverse_commands = False
        self.current = {
            'status': None,
            'percentage': None,
            'eta': None,
            'secondsLeft': None,
            'timeLeft': None,
            'layers': None,
            'currentLayer': None,
            'tsTimeLeft': None,
            'light': None,
            'power': None,
        }
        self.on_screen = {
            'status': None,
            'percentage': None,
            'eta': None,
            'secondsLeft': None,
            'timeLeft': None,
            'layers': None,
            'currentLayer': None,
            'tsTimeLeft': None,
            'light': None,
            'power': None,
        }
        self.colours = {
            'background': (100, 100, 150),
            'digit_background': (0, 0, 0),
            'border': (244, 244, 244)
        }
        self.icon = {
            'status_connected': Image.open('assets/image/printer3d/connected.png'),
            'status_disconnected': Image.open('assets/image/printer3d/disconnected.png'),
            'status_aborted': Image.open('assets/image/printer3d/abort.png'),
            'status_printed': Image.open('assets/image/printer3d/done.png'),
            'status_printing': Image.open('assets/image/printer3d/start.png'),
            'light_on': Image.open('assets/image/printer3d/lightbulb.png'),
            'power_on': Image.open('assets/image/printer3d/power_on.png'),
            'power_off': Image.open('assets/image/printer3d/power_off.png'),
        }
        self.width = 105
        self.height = 105
        self.initialized = False

    def draw_widget(self, lcd, pos_x, pos_y):
        """draw a tile"""
        lcd.background_color = self.colours['background']
        lcd.fill_rect(pos_x, pos_y, pos_x + 105, pos_y + 105)
        lcd.transparency_color = (0, 0, 0)

        lcd.color = self.colours['border']
        # lcd.draw_circle(pos_x + 36, pos_y + 40, 1)
        # lcd.draw_circle(pos_x + 36, pos_y + 50, 1)

        lcd.draw_circle(pos_x + 71, pos_y + 40, 1)
        lcd.draw_circle(pos_x + 71, pos_y + 50, 1)

        lcd.color = self.colours['border']
        lcd.draw_rect(pos_x, pos_y, pos_x + 105, pos_y + 105)

        self.draw_values(lcd, pos_x, pos_y, True)
        self.initialized = True

    def draw_values(self, lcd, pos_x, pos_y, force=False):
        # modify timeLeft according to ts
        if self.current['tsTimeLeft'] is not None \
                and self.current['timeLeft'] is not None and self.current['timeLeft'] != "0":
            now = datetime.datetime.now()
            d = datetime.datetime.now() - self.current['tsTimeLeft']
            if d.total_seconds() > 1:
                self.current['tsTimeLeft'] = now
                self.current['timeLeft'] = _decrease_time(self.current['timeLeft'], math.floor(d.total_seconds()))

        current = {
            'status': self.current['status'],
            'percentage': '00' if self.current['percentage'] is None else str(self.current['percentage']).rjust(2, '0'),
            'eta': self.current['eta'],
            'secondsLeft': self.current['secondsLeft'],
            'timeLeft': self.current['timeLeft'],
            'tsTimeLeft': self.current['tsTimeLeft'],
            'currentLayer': self.current['currentLayer'],
            'layers': self.current['layers'],
            'light': self.current['light'],
            'power': self.current['power'],
        }

        if force or self.on_screen['percentage'] != current['percentage']:
            if current['percentage'] == "100":
                current['percentage'] = "00"
            self.draw_number(
                lcd, pos_x+55, pos_y+3,
                self.font,
                current['percentage'],
                self.on_screen['percentage'],
                16,
                force
            )

        if (force or self.on_screen['status'] != current['status']) and current['status'] is not None:
            lcd.background_color = self.colours['background']
            lcd.fill_rect(pos_x + 7, pos_y + 5, pos_x + 30, pos_y + 25)
            lcd.transparency_color = (255, 255, 255)
            lcd.draw_image(pos_x + 7, pos_y + 5, self.icon['status_'+current['status']])

        if force or self._times_differ(current['timeLeft'], self.on_screen['timeLeft']):
            if current['timeLeft'] is not None:
                self.draw_number(
                    lcd, pos_x + 5, pos_y + 32, self.font, current['timeLeft'][0], self.on_screen['timeLeft'][0] if self.on_screen['timeLeft'] is not None else None, 15, force
                )
                self.draw_number(
                    lcd, pos_x + 40, pos_y + 32, self.font, current['timeLeft'][1], self.on_screen['timeLeft'][1] if self.on_screen['timeLeft'] is not None else None, 15, force
                )
                self.draw_number(
                    lcd, pos_x + 75, pos_y + 32, self.font, current['timeLeft'][2], self.on_screen['timeLeft'][2] if self.on_screen['timeLeft'] is not None else None, 15, force
                )

        if current['light'] is not None and (force or self.on_screen['light'] != current['light']):
            if current['light']:
                lcd.transparency_color = (0, 0, 0)
                lcd.draw_image(pos_x+7, pos_y+70, self.icon['light_on'])
            else:
                lcd.background_color = self.colours['background']
                lcd.fill_rect(pos_x + 7, pos_y + 70, pos_x + 30, pos_y + 100)

        if current['power'] is not None and (force or self.on_screen['power'] != current['power']):
            lcd.color = self.colours['background']
            lcd.fill_rect(pos_x+70, pos_y+70, pos_x+94, pos_y+96)
            if current['power']:
                lcd.transparency_color = (255, 255, 255)
                lcd.draw_image(pos_x + 70, pos_y + 70, self.icon['power_on'])
            else:
                lcd.transparency_color = (255, 255, 255)
                lcd.draw_image(pos_x + 70, pos_y + 70, self.icon['power_off'])

        self.on_screen = current.copy()

    def _times_differ(self, time_one, time_two):
        if time_one is None and time_two is None:
            return False

        if time_two is None and time_one is not None:
            return True

        if time_one[0] != time_two[0] or time_one[1] != time_two[1] or time_one[2] != time_two[2]:
            return True

        return False

    def update_values(self, values):
        if 'status' in values:
            self.current['status'] = values['status']
        if 'percentage' in values:
            self.current['percentage'] = values['percentage']
        if 'eta' in values:
            self.current['eta'] = values['eta']
        if 'secondsLeft' in values:
            self.current['secondsLeft'] = values['secondsLeft']
        if 'printTimeLeft' in values:
            self.current['timeLeft'] = _explode_time_left(values["printTimeLeft"])
            self.current['tsTimeLeft'] = datetime.datetime.now()
        if 'currentLayer' in values:
            self.current['currentLayer'] = values["currentLayer"]
        if 'totalLayers' in values:
            self.current['layers'] = values["totalLayers"]
        if 'relay' in values:
            if self.power_pin is not None:
                self.current['power'] = bool(values['relay'][self.power_pin])
                if self.reverse_relay:
                    self.current['power'] = not self.current['power']
            if self.light_pin is not None:
                self.current['light'] = bool(values['relay'][self.light_pin])
                if self.reverse_relay:
                    self.current['light'] = not  self.current['light']

    def action(self, name, pos_x, pos_y):
        if not self.light_pin:
            return

        if 0 < pos_x < 70 and 41 < pos_y < self.height:
            current_light = self.current['light']
            if self.reverse_commands:
                current_light = not current_light
            message = {
                'parameters': {
                    'channel': self.light_pin
                },
                'targets': [name],
                'event': "channel.off" if current_light else "channel.on"
            }

            comm.send(message)


def _decrease_time(time, seconds):
    out = ["00", "00", "00", "00"]
    step = [0, 24, 60, 60]
    rest = 0
    for idx in range(len(time) - 1, -1, -1):
        if time[idx] is not None:
            v = int(time[idx]) - seconds - rest
            seconds = 0
            rest = 0
            if v < 0:
                rest = 1
                v += step[idx]

            out[idx] = str(v).rjust(2, '0')

    if out[0] == "-1":
        out = ["00", "00", "00", "00"]

    return out


def _explode_time_left(time_left):
    if time_left is None or time_left == "0" or time_left == "-":
        return ["00", "00", "00"]
    try:
        match = re.match(r'(\d+d)*(\d+h)*(\d+m)*(\d+s)', time_left)
        parts = match.groups()
        days = (parts[0][:-1]).rjust(2, '0') if parts[0] is not None else '00'
        hours = (parts[1][:-1]).rjust(2, '0') if parts[1] is not None else '00'
        minutes = (parts[2][:-1]).rjust(2, '0') if parts[2] is not None else '00'
        seconds = (parts[3][:-1]).rjust(2, '0') if parts[3] is not None else '00'
    except TypeError as e:
        print(">>", time_left)
        raise e
    except AttributeError as e:
        print(">>", time_left)
        raise e

    return [days, hours, minutes, seconds]

