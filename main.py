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
from socket_conn.listener import Listener
import service.comm as comm
from service.exceptions import *
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    # filename='doton.log',
    level=logging.INFO
)
logging.debug('Starting')

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

listener = Listener(config.get('socket.address'))
window_manager = WindowManager(config.lcd, config.init_touch)

clock = Clock(FONTS['15x28'])
window_manager.add_widget('clock', clock, 0, 0)

kitchenNode = NodeOne(FONTS['24x42'])
window_manager.add_widget('node-kitchen', kitchenNode, 110, 0)
listener.add_widget('node-kitchen', kitchenNode)

northNode = NodeOne(FONTS['24x42'])
northNode.colours['background'] = (0, 100, 150)
window_manager.add_widget('node-lib', northNode, 220, 0)
listener.add_widget('node-lib', northNode)

livingNode = NodeOne(FONTS['24x42'])
livingNode.colours['background'] = (100, 100, 150)
window_manager.add_widget('node-living', livingNode, 330, 0)
listener.add_widget('node-living', livingNode)

openweatherNode = Openweather([0, 1], FONTS)
window_manager.add_widget('openweather', openweatherNode, 110, 107)
listener.add_widget('openweather', openweatherNode)

openAqNode = OpenAQ() #['Bielsko-Biała, ul.Partyzantów'])
window_manager.add_widget('openaq', openAqNode, 0, 50)
listener.add_widget('openaq', openAqNode)

# cr6Node = Printer3d(FONTS['12x25'])
# cr6Node.colours['border'] = (0, 0, 255)
# window_manager.add_widget('node-ce6cr', cr6Node, 110, 214)
# listener.add_widget('node-ce6cr', cr6Node)

ender5proNode = Printer3d(FONTS['12x25'], light_node_name="node-relaybox2", light_channel=1, power_node_name="node-relaybox2", power_channel=3)
ender5proNode.colours['border'] = (0, 0, 0)
window_manager.add_widget('ender5pro', ender5proNode, 220, 214)
listener.add_widget('ender5pro', ender5proNode)
listener.add_widget("node-relaybox2", ender5proNode)
listener.add_widget("node-printers", ender5proNode)

ender5plusNode = Printer3d(FONTS['12x25'], light_node_name="node-printers", light_channel=3, power_node_name="node-printers", power_channel=1)
ender5plusNode.colours['border'] = (255, 165, 0)
window_manager.add_widget('ender5plus', ender5plusNode, 330, 214)
listener.add_widget('ender5plus', ender5plusNode)
listener.add_widget("node-relaybox2", ender5plusNode)
listener.add_widget("node-printers", ender5plusNode)

try:
    listener.start()
    window_manager.start()

    while True:
        time.sleep(1)
        if listener.connection_error:
            window_manager.crash()
            raise ConnectionLost()
except KeyboardInterrupt:
    logging.debug('Closing')
except:
    logging.debug('Exception')
    raise
finally:
    logging.debug('finally')
    window_manager.stop()
    window_manager.join()

    listener.stop()
    listener.join()
