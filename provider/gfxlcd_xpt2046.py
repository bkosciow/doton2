from service.utils import *
from gfxlcd.driver.xpt2046.xpt2046 import XPT2046
# from gfxlcd.driver.ili9486.spi import SPI
# from gfxlcd.driver.ili9486.ili9486 import ILI9486
# from gfxlcd.driver.ili9325.gpio import GPIO
# from gfxlcd.driver.ili9325.ili9325 import ILI9325


class Provider(object):
    def __init__(self, config):
        self.config = config

    def provide(self, callback):
        size = self.config['size'].split(",")
        touch = XPT2046(
            int(size[0]), int(size[1]), int(self.config['irq']), callback, int(self.config['cs'])
        )
        touch.rotate = int(self.config['rotate'])
        touch.init()
