from .utils import *
from gfxlcd.driver.ili9486.spi import SPI
from gfxlcd.driver.ili9486.ili9486 import ILI9486
from gfxlcd.driver.ili9325.gpio import GPIO
from gfxlcd.driver.ili9325.ili9325 import ILI9325


class Provider(object):
    def __init__(self, config):
        self.config = config

    def provide_lcd(self):
        size = self.config['size'].split(",")
        drv = self._get_drv()
        lcd = None
        if self.config["type"] == "ili9486":
            lcd = ILI9486(int(size[0]), int(size[1]), drv)

        if self.config["type"] == "ili9325":
            lcd = ILI9325(int(size[0]), int(size[1]), drv)

        if lcd:
            lcd.rotation = int(self.config['rotate'])

        return lcd

    def _get_drv(self):
        driver_pins = string_to_dict(self.config['pins'])
        drv = None
        if self.config['driver'] == "spi":
            drv = SPI()
            if driver_pins:
                drv.pins = driver_pins

        if self.config['driver'] == "gpio":
            drv = GPIO()
            if driver_pins:
                drv.pins = driver_pins

        return drv
