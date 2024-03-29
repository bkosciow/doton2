import copy
from service.widget import Widget
from PIL import Image
from pprint import pprint
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)


class Openweather(Widget):
    """Openweathermap widget"""
    def __init__(self, forecast_days, fonts):
        super().__init__()
        self.forecast_days = forecast_days
        self.fonts = fonts
        self.colours = {
            'background_current': (127, 127, 0),
            'background_forecast': (0, 127, 127),
            'digit_background': (0, 0, 0),
            'border': (244, 244, 244)
        }
        self.current_weather = {
            'current': {
                'pressure': 0,
                'temperature_current': 0,
                'humidity': 0,
                'wind_speed': 0,
                'clouds': 0,
                'weather_id': 0,
                'update': 0,
                'wind_deg': 0,
                'weather': ''
            },
            'screen': None
        }
        self.forecast_weather = {}
        for day in forecast_days:
            self.forecast_weather[day] = {
                'current': {
                    'pressure': 0,
                    'clouds': 0,
                    'temperature_max': 0,
                    'wind_speed': 0,
                    'wind_deg': 0,
                    'temperature_min': 0,
                    'weather_id': 0,
                    'humidity': 0,
                    'weather': ''
                },
                'screen': None
            }

        self.icon = {
            'temperature': Image.open('assets/image/openweather/thermometer.png'),
            'compass': Image.open('assets/image/openweather/compass.png'),
            'cloud_empty': Image.open('assets/image/openweather/cloud_empty.png'),
            'cloud_full': Image.open('assets/image/openweather/cloud_full.png'),
            'drop_empty': Image.open('assets/image/openweather/drop_empty.png'),
            'drop_full': Image.open('assets/image/openweather/drop_full.png'),
            200: None, 201: None, 202: None, 210: None, 211: None,
            212: None, 221: None, 230: None, 231: None, 232: None,
            300: None, 301: None, 302: None, 310: None, 311: None,
            312: None, 313: None, 314: None, 321: None, 500: None,
            501: None, 502: None, 503: None, 504: None, 511: None,
            520: None, 521: None, 522: None, 531: None, 600: None,
            601: None, 602: None, 611: None, 612: None, 615: None,
            616: None, 620: None, 621: None, 622: None, 701: None,
            711: None, 721: None, 731: None, 741: None, 751: None,
            761: None, 762: None, 771: None, 781: None, 800: None,
            801: None, 802: None, 803: None, 804: None
        }
        self.initialized = False

    def draw_widget(self, lcd, pos_x, pos_y):
        """draw a tiles"""
        self._draw_widget(lcd, 'current', pos_x, pos_y)
        for idx in range(len(self.forecast_days)):
            self._draw_widget(lcd, 'forecast', pos_x + ((idx+1)*110), pos_y)
        self.draw_values(lcd, pos_x, pos_y, True)
        self.initialized = True

    def _draw_widget(self, lcd, widget_type, pos_x, pos_y):
        """draw a tile"""
        lcd.background_color = self.colours['background_'+widget_type]
        lcd.fill_rect(pos_x, pos_y, pos_x + 105, pos_y + 105)
        lcd.transparency_color = (0, 0, 0)
        lcd.draw_image(pos_x + 92, pos_y + 7, self.icon['temperature'])
        lcd.transparency_color = (255, 255, 255)
        lcd.color = self.colours['border']
        lcd.draw_rect(pos_x, pos_y, pos_x + 105, pos_y + 105)

    def draw_values(self, lcd, pos_x, pos_y, force=False):
        """draw values"""
        self._draw_values(lcd, 'current', 0, pos_x, pos_y, force)
        for idx in range(len(self.forecast_days)):
            self._draw_values(lcd, 'forecast', idx, pos_x + ((idx+1)*110), pos_y, force)

    def _draw_values(self, lcd, widget_type, day, pos_x, pos_y, force=False):
        """draw current values"""
        current = {
            'wind_speed': self._get_value(widget_type, day, 'current', 'wind_speed'),
            'wind_deg': self._degree_to_direction(
                widget_type, day, 'current', 'wind_deg'
            ),
            'clouds': self._get_value(widget_type, day, 'current', 'clouds', 2),
            'humidity': self._get_value(widget_type, day, 'current', 'humidity', 2),
            'pressure': self._get_value(widget_type, day, 'current', 'pressure', 4),
            'weather_id': self._get_value(widget_type, day, 'current', 'weather_id', 3),
        }
        screen = {
            'wind_speed': self._get_value(widget_type, day, 'screen', 'wind_speed'),
            'wind_deg': self._degree_to_direction(
                widget_type, day, 'screen', 'wind_deg'
            ),
            'clouds': self._get_value(widget_type, day, 'screen', 'clouds', 2),
            'humidity': self._get_value(widget_type, day, 'screen', 'humidity', 2),
            'pressure': self._get_value(widget_type, day, 'screen', 'pressure', 4),
            'weather_id': self._get_value(widget_type, day, 'screen', 'weather_id', 3)
        }
        if widget_type == 'current':
            current['temperature_current'] = self._get_value(
                widget_type, day, 'current', 'temperature_current'
            )
            screen['temperature_current'] = self._get_value(
                widget_type, day, 'screen', 'temperature_current'
            )
        else:
            current['temperature_max'] = self._get_value(
                widget_type, day, 'current', 'temperature_max'
            )
            screen['temperature_max'] = self._get_value(
                widget_type, day, 'screen', 'temperature_max'
            )

        if widget_type == 'current':
            if force or screen['temperature_current'] is None or current['temperature_current'] != screen['temperature_current']:
                if screen['temperature_current'] is not None and self._get_font(current['temperature_current']) != self._get_font(screen['temperature_current']):
                    force = True
                self.draw_number(
                    lcd, pos_x+50, pos_y+5,
                    self._get_font(current['temperature_current']),
                    self._get_abs_value(current['temperature_current']),
                    screen['temperature_current'],
                    20,
                    force
                )
        else:
            if force or screen['temperature_max'] is None or current['temperature_max'] != screen['temperature_max']:
                if screen['temperature_max'] is not None and self._get_font(current['temperature_max']) != self._get_font(screen['temperature_max']):
                    force = True
                self.draw_number(
                    lcd, pos_x+50, pos_y+5,
                    self._get_font(current['temperature_max']),
                    self._get_abs_value(current['temperature_max']),
                    screen['temperature_max'],
                    20,
                    force
                )

        if force or screen['wind_speed'] is None or current['wind_speed'] != screen['wind_speed']:
            self.draw_number(
                lcd, pos_x+45, pos_y+39, self.fonts['15x28'],
                current['wind_speed'], screen['wind_speed'], 20,
                force
            )

        if force or screen['wind_deg'] is None or current['wind_deg'] != screen['wind_deg']:
            lcd.background_color = self.colours['background_'+widget_type]
            lcd.fill_rect(pos_x+84, pos_y+44, pos_x+99, pos_y+65)
            lcd.transparency_color = ((255, 255, 255), (0, 0, 0))
            lcd.draw_image(
                pos_x + 84, pos_y + 44,
                self.icon['compass'].rotate(
                    -1 * self._wind_degree(widget_type, day)
                )
            )

        if force or screen['clouds'] is None or current['clouds'] != screen['clouds']:
            width, height = self.icon['cloud_full'].size
            lcd.background_color = self.colours['background_'+widget_type]
            lcd.fill_rect(pos_x+1, pos_y+47, pos_x+1+width, pos_y+47+height)
            lcd.transparency_color = (255, 255, 255)
            lcd.draw_image(pos_x+1, pos_y+47, self.icon['cloud_empty'])
            new_width = round(width * int(current['clouds']) / 100)
            lcd.draw_image(
                pos_x+1, pos_y+47,
                self.icon['cloud_full'].crop((0, 0, new_width, height))
            )

        if force or screen['humidity'] is None or current['humidity'] != screen['humidity']:
            width, height = self.icon['drop_full'].size
            lcd.background_color = self.colours['background_'+widget_type]
            lcd.fill_rect(pos_x+3, pos_y+74, pos_x+3+width, pos_y+74+height)
            lcd.transparency_color = (255, 255, 255)
            lcd.draw_image(pos_x + 3, pos_y + 74, self.icon['drop_empty'])
            new_height = height - round(height * int(current['humidity']) / 100)
            lcd.draw_image(
                pos_x + 3, pos_y + 74 + new_height,
                self.icon['drop_full'].crop((0, new_height, width, height))
            )

        if force or screen['pressure'] is None or current['pressure'] != screen['pressure']:
            self.draw_number(
                lcd, pos_x+25, pos_y+72, self.fonts['15x28'],
                current['pressure'], screen['pressure'], 20,
                force
            )

        if current['weather_id'] is not None:
            current['weather_id'] = int(current['weather_id'])
        if screen['weather_id'] is not None:
            screen['weather_id'] = int(screen['weather_id'])
        if current['weather_id'] != 0 and (force or screen['weather_id'] is None or current['weather_id'] != screen['weather_id']):
            lcd.background_color = self.colours['background_'+widget_type]
            lcd.fill_rect(pos_x+2, pos_y+3, pos_x+42, pos_y+43)
            lcd.transparency_color = (255, 255, 255)
            lcd.draw_image(pos_x+2, pos_y+3, self._get_weather_icon(current['weather_id']))

        if widget_type == 'current':
            self.current_weather['screen'] = self.current_weather['current'].copy()
        else:
            self.forecast_weather[day]['screen'] = self.forecast_weather[day]['current'].copy()

    def _get_font(self, value):
        """return red font for value >0 or blue font for <=0 """
        return self.fonts['15x28_red'] if int(value) > 0 else self.fonts['15x28_blue']

    def _get_abs_value(self, value):
        """return abs value from string-number"""
        return value if value[0] != '-' else value[1:]

    def _get_value(self, widget_type, day, key, value, precision=2):
        """get value"""
        sign = ''
        if widget_type == 'current':
            if self.current_weather[key] is None:
                return None
            value = self.current_weather[key][value]
        else:
            if self.forecast_weather[day][key] is None:
                return None
            value = self.forecast_weather[day][key][value]

        if value < 0:
            sign = '-'
            value *= -1
        value = str(round(value)).rjust(precision, '0')

        return sign + value

    def _wind_degree(self, widget_type, day):
        """return wind degree value"""
        if widget_type == 'current':
            return self.current_weather['current']['wind_deg']
        else:
            return self.forecast_weather[day]['current']['wind_deg']

    def _degree_to_direction(self, widget_type, day, key, value):
        """degree to direction"""
        degree = 0
        if widget_type == 'current':
            degree = 0 if self.current_weather[key] is None \
                else round(self.current_weather[key][value])

        if widget_type == 'forecast':
            degree = 0 if self.forecast_weather[day][key] is None \
                else round(self.forecast_weather[day][key][value])

        if 348.75 <= degree or degree < 11.25:
            return 'N'
        elif 11.25 <= degree < 33.75:
            return 'NNE'
        elif 33.75 <= degree < 56.25:
            return 'NE'
        elif 56.25 <= degree < 78.75:
            return 'ENE'
        elif 78.75 <= degree < 101.25:
            return 'E'
        elif 101.25 <= degree < 123.75:
            return 'ESE'
        elif 123.75 <= degree < 146.25:
            return 'SE'
        elif 146.25 <= degree < 168.75:
            return 'SSE'
        elif 168.75 <= degree < 191.25:
            return 'S'
        elif 191.25 <= degree < 213.75:
            return 'SSW'
        elif 213.75 <= degree < 236.25:
            return 'SW'
        elif 236.25 <= degree < 258.75:
            return 'WSW'
        elif 258.75 <= degree < 281.25:
            return 'W'
        elif 281.25 <= degree < 303.75:
            return 'WNW'
        elif 303.75 <= degree < 326.25:
            return 'NW'
        elif 326.25 <= degree < 348.75:
            return 'NNW'

    def update_values(self, values, name=""):
        try:
            if values is None:
                logger.error('weather null')
                print("Weather null value")
                return
            if 'current' in values and values['current'] is not None:
                logger.debug('current weather')
                self.current_weather['current'] = values['current']

            if 'forecast' in values and values['forecast'] is not None:
                logger.debug('forecast weather')
                today = datetime.today()
                for offset in self.forecast_days:
                    date = today + timedelta(days=offset)
                    date = date.strftime('%Y-%m-%d')
                    if date in values['forecast']:
                        self.forecast_weather[offset]['current'] = values['forecast'][date]
        except:
            # print(values)
            logger.error('exception')
            logger.exception('values errror')
            raise

    def _get_weather_icon(self, status):
        """load weather icon when needed"""
        if self.icon[status] is None:
            self.icon[status] = Image.open('assets/image/openweather/'+str(status)+".png")

        return self.icon[status]
