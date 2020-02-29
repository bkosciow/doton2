"""Config parser fle"""
from configparser import ConfigParser
from importlib import import_module
from .utils import *


class Config(object):
    """Class Config"""
    def __init__(self, file="config.ini"):
        self.file = file
        self.config = ConfigParser()
        self.config.read(file)
        self.lcd = None
        self.touch = None
        self.init_lcd()

    def get(self, name):
        if "." in name:
            section, name = name.split(".")
        else:
            section = "global"

        val = self.config.get(section, name)
        return val if val != "" else None

    def __getitem__(self, item):
        return self.config[item]

    def get_section(self, section):
        """return section"""
        return dict(self.config.items(section))

    def init_lcd(self):
        """dynamically load and init lcd"""
        lcd_config = self.get_section(self.get("global.lcd"))
        path = lcd_config['provider']
        provider = getattr(import_module(path), "Provider")
        p = provider(lcd_config)
        self.lcd = p.provide_lcd()
        if self.lcd is None:
            raise UnsuportedLCD("Unsupported lcd")

        self.lcd.init()

    # def init_touch(self, callback):
    #     """dynamically load and init touch panel"""
    #     driver_name = self.config.get('touch', 'driver')
    #     size = self.config.get('touch', 'size').split(",")
    #     cs = self.config.get('touch', 'cs')
    #     if cs == '':
    #         cs = None
    #     else:
    #         cs = int(self.config.get('touch', 'cs'))
    #     path = "gfxlcd.driver.{}.{}".format(driver_name, driver_name)
    #     class_ = getattr(import_module(path), driver_name.upper())
    #     driver = class_(
    #         int(size[0]), int(size[1]),
    #         int(self.config.get('touch', 'irq')),
    #         callback,
    #         cs
    #     )
    #     driver.rotate = int(self.config.get('touch', 'rotate'))
    #     driver.init()

    def get_dict(self, name):
        value = self.get(name)
        return string_to_dict(value)


class UnsuportedLCD(Exception):
    pass
