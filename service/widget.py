"""An abstract for Widget class"""
import abc


class Widget(metaclass=abc.ABCMeta):

    def __init__(self):
        self.encoder_idx = 0
        self.width = 0
        self.height = 0

    """Widget abstract"""
    @abc.abstractmethod
    def draw_widget(self, lcd, pos_x, pos_y):
        """draw a tile"""
        pass

    @abc.abstractmethod
    def draw_values(self, lcd, pos_x, pos_y, force=False):
        """draw a changed values. With force must redraw all values"""
        pass

    @abc.abstractmethod
    def update_values(self, values, name=""):
        """change a value, values is a dict [name] = value"""
        pass

    def draw_number(self, lcd, pos_x, pos_y, font, new, old, spacing=30, force=False):
        """draw a number"""
        lcd.transparency_color = font.get_transparency()
        for idx in range(0, len(new)):
            if force or old is None or new[idx] != old[idx]:
                lcd.draw_image(
                    pos_x + (idx * spacing),
                    pos_y,
                    font.get(int(new[idx]))
                )


class Clickable(metaclass=abc.ABCMeta):
    """Interface for clickable widget"""
    @abc.abstractmethod
    def action(self, name, pos_x, pos_y):
        """action for touch"""
        return
