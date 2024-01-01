from service.widget import Widget, Clickable
from PIL import Image
import re
import datetime
import math
import service.comm as comm
from datetime import datetime, timedelta


class Printer3d(Widget, Clickable):

    def __init__(self, font,
                 light_node_name=None, light_channel=0, light_reversed=False,
                 power_node_name=None, power_channel=0, power_reversed=False):
        super().__init__()
        self.font = font
        self.work = True
        self.light = {
            "node_name": light_node_name,
            "channel": light_channel,
            "reversed": light_reversed
        }
        self.power = {
            "node_name": power_node_name,
            "channel": power_channel,
            "reversed": power_reversed
        }
        self.current = {
            'status': None,
            'percentage': None,
            'secondsLeft': None,
            'timeLeft': None,
            'light': None,
            'power': None,
        }
        self.on_screen = {
            'status': None,
            'percentage': None,
            'secondsLeft': None,
            'timeLeft': None,
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

        lcd.draw_circle(pos_x + 71, pos_y + 40, 1)
        lcd.draw_circle(pos_x + 71, pos_y + 50, 1)

        lcd.color = self.colours['border']
        lcd.draw_rect(pos_x, pos_y, pos_x + 105, pos_y + 105)

        self.draw_values(lcd, pos_x, pos_y, True)
        self.initialized = True

    def draw_values(self, lcd, pos_x, pos_y, force=False):
        current = {
            'status': self.current['status'],
            'percentage': '00' if self.current['percentage'] is None else str(self.current['percentage']).rjust(2, '0'),
            'timeLeft': self.current['timeLeft'],
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
                    lcd, pos_x + 24, pos_y + 32, self.font, current['timeLeft'][0], self.on_screen['timeLeft'][0] if self.on_screen['timeLeft'] is not None else None, 15, force
                )
                self.draw_number(
                    lcd, pos_x + 75, pos_y + 32, self.font, current['timeLeft'][1], self.on_screen['timeLeft'][1] if self.on_screen['timeLeft'] is not None else None, 15, force
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

        if time_one[0] != time_two[0] or time_one[1] != time_two[1]:
            return True

        return False

    def update_values(self, values, name=""):
        if 'error' in values:
            if values['error']:
                if 'error_message' in values and values['error_message'] != '':
                    self.current['status'] = "disconnected"
                else:
                    self.current['status'] = "disconnected"
            else:
                self.current['status'] = "connected"
                if 'status' in values:
                    if values['flags']['printing'] or values['flags']['pausing'] or values['flags']['paused']:
                        self.current['status'] = "printing"
                        self.current['percentage'] = round(values['print']['completion'])
                        self.current['timeLeft'] = str(timedelta(seconds=values['print']['printTimeLeft'])).split(':')[:2]
                        self.current['timeLeft'][0] = self.current['timeLeft'][0].rjust(3, '0')
                        self.current['timeLeft'][1] = self.current['timeLeft'][1].rjust(2, '0')
                        if float(values['print']['completion']) > 99.8:
                            self.current['status'] = "printed"
                    else:
                        self.current['percentage'] = 0
                        self.current['timeLeft'] = ['000', '00']

        if self.light is not None and "relay" in values:
            if name == self.light['node_name']:
                self.current['light'] = bool(values['relay'][self.light['channel']])

        if self.power is not None and "relay" in values:
            if name == self.power['node_name']:
                self.current['power'] = bool(values['relay'][self.power['channel']])

    def action(self, name, pos_x, pos_y):
        if not self.light["node_name"]:
            return

        if 0 < pos_x < self.width and 41 < pos_y < self.height:
            current_light = self.current['light']
            if self.light["reversed"]:
                current_light = not current_light
            message = {
                'parameters': {
                    'channel': self.light["channel"]
                },
                'targets': [self.light["node_name"]],
                'event': "channel.off" if current_light else "channel.on"
            }

            comm.send(message)
