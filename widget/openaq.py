from service.widget import Widget
from PIL import Image


class OpenAQ(Widget):
    """Class NodeOne"""
    def __init__(self, group=None):
        super().__init__()
        self.group = group
        self.colours = {
            'background': (160, 160, 160),
            'border': (244, 244, 244),
            0: (0, 127, 14),
            1: (0, 209, 14),
            2: (255, 216, 0),
            3: (255, 106, 0),
            4: (255, 0, 0),
            5: (127, 0, 0)
        }
        self.current = {
            'PM25': None,
            'PM10': None,
            'O3': None,
            'SO2': None,
            'CO': None,
            'NO2': None,
            'highest_index': None,
        }
        self.screen = {
            'PM25': None,
            'PM10': None,
            'O3': None,
            'SO2': None,
            'CO': None,
            'NO2': None,
            'highest_index': None,
        }
        self.icon = {
            'index_0': Image.open('assets/image/airquality/index_0.png'),
            'index_1': Image.open('assets/image/airquality/index_1.png'),
            'index_2': Image.open('assets/image/airquality/index_2.png'),
            'index_3': Image.open('assets/image/airquality/index_3.png'),
            'index_4': Image.open('assets/image/airquality/index_4.png'),
            'index_5': Image.open('assets/image/airquality/index_5.png'),
        }

        for i in range(0, 5):
            for item in [['pm25', 0, 36], ['pm10', 39, 74], ['o3', 76, 93], ['so2', 96, 121], ['co', 124, 142], ['no2', 145, 170]]:
                self.icon[item[0] + "_" + str(i)] = self.icon['index_' + str(i)].crop((item[1], 0, item[2], 13))

        self.initialized = False

    def draw_widget(self, lcd, pos_x, pos_y):
        """draw a tile"""
        lcd.background_color = self.colours['background']
        lcd.fill_rect(pos_x, pos_y, pos_x + 105, pos_y + 35)

        lcd.color = self.colours['border']
        lcd.draw_rect(pos_x, pos_y, pos_x + 105, pos_y + 35)
        lcd.draw_rect(pos_x + 1, pos_y + 1, pos_x + 104, pos_y + 34)

        self.draw_values(lcd, pos_x, pos_y, True)
        self.initialized = True

    def draw_values(self, lcd, pos_x, pos_y, force=False):
        lcd.transparency_color = (160, 160, 160)
        current = {
            'PM25': self.current['PM25'],
            'PM10': self.current['PM10'],
            'O3': self.current['O3'],
            'SO2': self.current['SO2'],
            'CO': self.current['CO'],
            'NO2': self.current['NO2'],
            'highest_index': self.current['highest_index']
        }

        if current['PM25'] is not None and (force or current['PM25'] != self.screen['PM25']):
            lcd.draw_image(pos_x + 4, pos_y + 3, self.icon['pm25_' + str(current['PM25'])])

        if current['PM10'] is not None and (force or current['PM10'] != self.screen['PM10']):
            lcd.draw_image(pos_x + 4, pos_y + 20, self.icon['pm10_' + str(current['PM10'])])

        if current['O3'] is not None and (force or current['O3'] != self.screen['O3']):
            lcd.draw_image(pos_x + 46, pos_y + 3, self.icon['o3_' + str(current['O3'])])

        if current['SO2'] is not None and (force or current['SO2'] != self.screen['SO2']):
            lcd.draw_image(pos_x + 72, pos_y + 3, self.icon['so2_' + str(current['SO2'])])

        if current['CO'] is not None and (force or current['CO'] != self.screen['CO']):
            lcd.draw_image(pos_x + 46, pos_y + 20, self.icon['co_' + str(current['CO'])])

        if current['NO2'] is not None and (force or current['NO2'] != self.screen['NO2']):
            lcd.draw_image(pos_x + 72, pos_y + 20, self.icon['no2_' + str(current['NO2'])])

        if force or current['highest_index'] != self.screen['highest_index']:
            lcd.color = self.colours[current['highest_index']]
            lcd.draw_rect(pos_x, pos_y, pos_x + 105, pos_y + 35)
            lcd.draw_rect(pos_x + 1, pos_y + 1, pos_x + 104, pos_y + 34)

        self.screen = current.copy()

    def update_values(self, values):
        highest_index = 0
        for location in values:
            if self.group is None or location in self.group:
                data = values[location]
                for item in data:
                    if data[item] is not None:
                        if item in self.current and (self.current[item] is None or self.current[item] < data[item]['index']):
                            self.current[item] = data[item]['index']
                        if item in self.current and highest_index < data[item]['index']:
                            highest_index = data[item]['index']

        self.current['highest_index'] = highest_index