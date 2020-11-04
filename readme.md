Doton2
===

Doton2 project is a control Node for IoT devices. It works on Raspberry Pi and uses ILI9328 or ILI9486 compatible display to show
information in a form of widget/tile.

[Articles](https://koscis.wordpress.com/tag/doton2/)

T

## Structure

assets - images

service - Config

view - NodeOne, Openweather, Clock, OpenAQ

## Configuration

File **config.ini** 

    [display_ili9486_spi]
    provider=provider.gfxlcd_lcd
    type=ili9486
    size=320,480
    rotate=270
    driver=spi
    pins={"CS": 8,"RST": 25,"RS": 24,"LED": ""}
    
    [display_cili9486_spi]
    provider=provider.gfxcili_lcd
    type=ili9486
    size=320,480
    rotate=270
    driver=spi
    pins=0, 3200000, 8, 25, 24
    
    [display_ili9325_gpio]
    provider=provider.gfxlcd_lcd
    type=ili9325
    size=320,240
    rotate=270
    driver=gpio
    pins={"RS": 27,"W": 17,"DB8": 22,"DB9": 23,"DB10": 24,"DB11": 5,"DB12": 12,"DB13": 16,"DB14": 20,"DB15": 21,"RST": 25,"LED": 6,"CS": 18}
    
    [touch_xpt2046]
    ;xpt2046 ad7843
    provider=provider.gfxlcd_xpt2046
    ;driver=xpt2046
    size=480,320
    rotate=0
    irq=17
    cs=7
    
    [global]
    ip=192.168.1.255
    port=5053
    node_name=control-node
    lcd=display_cili9486_spi
    touch=touch_xpt2046
    
    [grpc]
    address=192.168.1.202:8765
 
### Credits

Weather icons made by [Freepik](http://www.flaticon.com/authors/freepik) and [Linector](http://www.flaticon.com/authors/linector) from [www.flaticon.com](http://www.flaticon.com)
 
 

