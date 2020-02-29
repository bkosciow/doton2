Doton2
===

Doton2 project is a control Node for IoT devices. It works on Raspberry Pi and uses ILI9328 or ILI9486 compatible display to show
information in a form of widget/tile.

[Articles](https://koscis.wordpress.com/tag/doton2/)

T

## Structure

assets - images

service - Window Manager, Config

view - NodeOne, Openweather, Clock, Relay

## Configuration

File **config.ini** 

    [lcd]
    ;ili9486  ili9325
    lcd=ili9486
    size=320,480
    rotate=270
    driver=spi
    driver_pins={"CS": 8,"RST": 25,"RS": 24,"LED": ""}
    
    [touch]
    ;xpt2046 ad7843
    driver=xpt2046
    size=480, 320
    rotate=0
    irq=17
    cs=7
    
    [general]
    ;broadcast address
    ip=192.168.1.255
    port=5053
    node_name=control-node-2

    [grpc]
    address=192.168.1.202:8765
 
### Credits

Weather icons made by [Freepik](http://www.flaticon.com/authors/freepik) and [Linector](http://www.flaticon.com/authors/linector) from [www.flaticon.com](http://www.flaticon.com)
 
 

