"""Config parser fle"""
from configparser import ConfigParser
from importlib import import_module
from .utils import *
from iot_message.message import Message


class Config(object):
    """Class Config"""
    def __init__(self, file="config.ini"):
        self.file = file
        self.config = ConfigParser()
        self.config.read(file)
        self.lcd = None
        self.touch = None
        self.init_lcd()
        self.init_message()

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
        lcd_config = self.get_section(self.get("global.lcd"))
        path = lcd_config['provider']
        provider = getattr(import_module(path), "Provider")
        p = provider(lcd_config)
        self.lcd = p.provide()
        if self.lcd is None:
            raise UnsupportedLCD("Unsupported lcd")

        self.lcd.init()

    def init_touch(self, callback):
        touch_config = self.get_section(self.get("global.touch"))
        if touch_config is not None:
            path = touch_config['provider']
            provider = getattr(import_module(path), "Provider")
            p = provider(touch_config)
            p.provide(callback)

    def get_dict(self, name):
        value = self.get(name)
        return string_to_dict(value)

    def init_message(self):
        Message.node_name = self.get("message.node_name")
        if self.get("message.encoder"):
            encClass = getattr(import_module(self.get("message.encoder")), "Cryptor")
            params = self.get("message.encoder_params")
            if params is None:
                encInstance = encClass()
            else:
                params = params.split(",")
                encInstance = encClass(*params)

            Message.add_encoder(encInstance)


class UnsupportedLCD(Exception):
    pass
