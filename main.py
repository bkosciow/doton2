import RPi.GPIO as GPIO
import time
import socket
from widget.nodeone import NodeOne
from widget.openweather import Openweather
from widget.openaq import OpenAQ
from widget.printer3d import Printer3d
# from view.relay_widget import RelayWidget
from widget.clock import Clock
from gfxlcd_fonts import numbers_24x42
from gfxlcd_fonts import numbers_15x28
from gfxlcd_fonts import numbers_15x28_red
from gfxlcd_fonts import numbers_15x28_blue
from gfxlcd_fonts import numbers_12x25
from display.window_manager import WindowManager
from service.config import Config
from connector.listener import Listener
import service.comm as comm

GPIO.setmode(GPIO.BCM)

config = Config()
FONTS = {
    '24x42': numbers_24x42.Numbers(),
    '15x28': numbers_15x28.Numbers(),
    '15x28_red': numbers_15x28_red.Numbers(),
    '15x28_blue': numbers_15x28_blue.Numbers(),
    '12x25': numbers_12x25.Numbers(),
}
# FONTS['12x25'].transparency = ((1, 1, 1), (0, 0, 0), (64, 64, 64))

comm.address = (config.get("message.ip"), int(config.get("message.port")))

listener = Listener(config.get('grpc.address'))
window_manager = WindowManager(config.lcd, config.init_touch)

# clock = Clock(FONTS['15x28'])
# window_manager.add_widget('clock', clock, 0, 0)

# kitchenNode = NodeOne(FONTS['24x42'])
# window_manager.add_widget('node-kitchen', kitchenNode, 110, 0)
# listener.add_widget('node-kitchen', kitchenNode)
#
# northNode = NodeOne(FONTS['24x42'])
# northNode.colours['background'] = (0, 100, 150)
# window_manager.add_widget('node-north', northNode, 220, 0)
# listener.add_widget('node-north', northNode)
#
# livingNode = NodeOne(FONTS['24x42'])
# livingNode.colours['background'] = (100, 100, 150)
# window_manager.add_widget('node-living', livingNode, 330, 0)
# listener.add_widget('node-living', livingNode)
#
# openweatherNode = Openweather([0, 1, 2], FONTS)
# window_manager.add_widget('openweather', openweatherNode, 0, 107)
# listener.add_widget('openweather', openweatherNode)

# 'Bielsko-Biała, ul. Kossak-Szczuckiej 19'
# 'Bielsko-Biała, ul.Partyzantów'

# openAqNode = OpenAQ() #['Bielsko-Biała, ul.Partyzantów'])
# window_manager.add_widget('openaq', openAqNode, 0, 50)
# listener.add_widget('openaq', openAqNode)

cr6Node = Printer3d(FONTS['12x25'])
window_manager.add_widget('node-ce6cr', cr6Node, 0, 200)
listener.add_widget('node-ce6cr', cr6Node)


Dummy3dNode = Printer3d(FONTS['12x25'])
window_manager.add_widget('DummyPrinter', Dummy3dNode, 110, 200)
listener.add_widget('DummyPrinter', Dummy3dNode)

ender5proNode = Printer3d(FONTS['12x25'])
window_manager.add_widget('node-ender5pro', ender5proNode, 220, 200)
listener.add_widget('node-ender5pro', ender5proNode)

listener.start()

# config.init_touch(None)
# broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# address = (config.get('ip', '<broadcast>'), int(config.get('port')))
#

# exit(1)
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
