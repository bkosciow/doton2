import gfxcili.ili9486
import gfxcili.ili9325


class Provider(object):
    def __init__(self, config):
        self.config = config

    def provide(self):
        size = self.config['size'].split(",")
        driver_pins = [int(pin.strip()) for pin in self.config['pins'].split(",")]
        driver_pins.insert(0, int(size[1]))
        driver_pins.insert(0, int(size[0]))
        lcd = None
        if self.config["type"] == "ili9486":
            lcd = gfxcili.ili9486.ili9486(*driver_pins)

        if self.config["type"] == "ili9325":
            lcd = gfxcili.ili9325.ili9325(*driver_pins)

        if lcd:
            lcd.rotation = int(self.config['rotate'])

        return lcd

