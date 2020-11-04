"""Widget for Node One sensor. Displas data from it in form of tile"""
from service.widget import Widget, Clickable
from PIL import Image
import service.comm as comm


class NodeOne(Widget, Clickable):
    """Class NodeOne"""
    def __init__(self, font):
        super().__init__()
        self.font = font
        self.colours = {
            'background': (255, 250, 0),
            'digit_background': (0, 0, 0),
            'border': (244, 244, 244)
        }
        self.current = {
            'temperature': 0,
            'humidity': 0,
            'movement': False,
            'light': False,
            'power': False,
        }
        self.screen = {
            'temperature': None,
            'humidity': None,
            'movement': None,
            'light': None,
            'power': None,
        }
        self.icon = {
            'movement': Image.open('assets/image/nodeone/movement.png'),
            'light': Image.open('assets/image/nodeone/lightbulb.png'),
            'temperature': Image.open('assets/image/nodeone/thermometer.png'),
            'humidity': Image.open('assets/image/nodeone/humidity.png'),
            'power': Image.open('assets/image/nodeone/power.png')
        }
        self.width = 105
        self.height = 105
        self.initialized = False

    def draw_widget(self, lcd, pos_x, pos_y):
        """draw a tile"""
        lcd.background_color = self.colours['background']
        lcd.fill_rect(pos_x, pos_y, pos_x + 105, pos_y + 105)

        lcd.background_color = self.colours['digit_background']
        lcd.fill_rect(pos_x+35, pos_y+5, pos_x+57, pos_y+46)
        lcd.fill_rect(pos_x+62, pos_y+5, pos_x+84, pos_y+46)
        lcd.fill_rect(pos_x+35, pos_y+55, pos_x+57, pos_y+95)
        lcd.fill_rect(pos_x+62, pos_y+55, pos_x+84, pos_y+95)

        lcd.transparency_color = (0, 0, 0)
        lcd.draw_image(pos_x + 91, pos_y + 10, self.icon['temperature'])
        lcd.draw_image(pos_x + 88, pos_y + 58, self.icon['humidity'])

        lcd.color = self.colours['border']
        lcd.draw_rect(pos_x, pos_y, pos_x + 105, pos_y + 105)

        self.draw_values(lcd, pos_x, pos_y, True)
        self.initialized = True

    def draw_values(self, lcd, pos_x, pos_y, force=False):
        """draw values"""
        current = {
            'temperature': str(self.current['temperature']).rjust(2, '0'),
            'humidity': str(self.current['humidity']).rjust(2, '0'),
            'movement': self.current['movement'],
            'light': self.current['light'],
            'power': self.current['power'],
        }
        screen = {
            'temperature': None if self.screen['temperature'] is None
            else str(self.screen['temperature']).rjust(2, '0'),
            'humidity': None if self.screen['humidity'] is None
            else str(self.screen['humidity']).rjust(2, '0'),
            'movement': self.screen['movement'],
            'light': self.screen['light'],
            'power': self.screen['power'],

        }
        lcd.transparency_color = self.font.get_transparency()
        if force or current['temperature'] != screen['temperature']:
            self.draw_number(
                lcd, pos_x + 35, pos_y + 5, self.font,
                current['temperature'], screen['temperature'], 27,
                force
            )

        if force or current['humidity'] != screen['humidity']:
            self.draw_number(
                lcd, pos_x + 35, pos_y + 55, self.font,
                current['humidity'], screen['humidity'], 27,
                force
            )

        if force or current['light'] != screen['light']:
            if current['light']:
                lcd.transparency_color = (0, 0, 0)
                lcd.draw_image(pos_x + 7, pos_y + 5, self.icon['light'])
            else:
                lcd.background_color = self.colours['background']
                lcd.fill_rect(pos_x+7, pos_y+5, pos_x+27, pos_y+25)

        if force or current['movement'] != screen['movement']:
            if current['movement']:
                lcd.transparency_color = (0, 0, 0)
                lcd.draw_image(pos_x + 7, pos_y + 30, self.icon['movement'])
            else:
                lcd.background_color = self.colours['background']
                lcd.fill_rect(pos_x+7, pos_y+30, pos_x+27, pos_y+50)

        if force or current['power'] != screen['power']:
            if current['power']:
                lcd.transparency_color = (0, 0, 0)
                lcd.draw_image(pos_x + 7, pos_y + 65, self.icon['power'])
            else:
                lcd.background_color = self.colours['background']
                lcd.fill_rect(pos_x + 7, pos_y + 65, pos_x + 27, pos_y + 85)

        self.screen = current.copy()

    def update_values(self, values):
        """change values"""
        # if not self.initialized:
        #     return
        if 'temp' in values:
            self.current['temperature'] = values['temp']

        if 'humi' in values:
            self.current['humidity'] = values['humi']

        if 'pir' in values:
            self.current['movement'] = values['pir']

        if 'light' in values:
            self.current['light'] = values['light']

        if 'relay' in values:
            self.current['power'] = True if values['relay'][0] else False

    def action(self, name, pos_x, pos_y):
        if 0 < pos_x < 50 and 51 < pos_y < self.height:
            message = {
                'parameters': {
                    'channel': 0
                },
                'targets': [name],
                'event': "channel.off" if self.current['power'] else "channel.on"
            }

            comm.send(message)
