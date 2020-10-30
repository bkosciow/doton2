import RPi.GPIO as GPIO
import time
import socket
from widget.nodeone import NodeOne
from widget.openweather import Openweather
# from view.relay_widget import RelayWidget
from widget.clock import Clock
from gfxlcd_fonts import numbers_24x42
from gfxlcd_fonts import numbers_15x28
from gfxlcd_fonts import numbers_15x28_red
from gfxlcd_fonts import numbers_15x28_blue
# from message_listener.server import Server
# from iot_message.message import Message
# from service.handler_dispatcher import HandlerDispatcher
from display.window_manager import WindowManager
from service.config import Config
from connector.listener import Listener

GPIO.setmode(GPIO.BCM)

config = Config()
FONTS = {
    '24x42': numbers_24x42.Numbers(),
    '15x28': numbers_15x28.Numbers(),
    '15x28_red': numbers_15x28_red.Numbers(),
    '15x28_blue': numbers_15x28_blue.Numbers(),
}

listener = Listener(config.get('grpc.address'))
listener.start()

window_manager = WindowManager(config.lcd)

clock = Clock(FONTS['15x28'])
window_manager.add_widget('clock', clock, 0, 0)

kitchenNode = NodeOne(FONTS['24x42'])
window_manager.add_widget('kitchen', kitchenNode, 110, 0)
listener.add_widget('node-kitchen', kitchenNode)

northNode = NodeOne(FONTS['24x42'])
northNode.colours['background'] = (0, 100, 150)
window_manager.add_widget('north', northNode, 220, 0)
listener.add_widget('node-north', northNode)

openweatherNode = Openweather([1, 2], FONTS)
window_manager.add_widget('openweather', openweatherNode, 0, 110)


# config.init_touch(None)
# broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# address = (config.get('ip', '<broadcast>'), int(config.get('port')))
#

#
window_manager.start()
#
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("closing...")
except:
    raise
finally:
    pass
    # workerHandler.stop()
    window_manager.stop()
    window_manager.join()

    listener.stop()
    listener.join()
    # workerHandler.join()
    # svr.join()
