import logging

from strip.basestrip import BaseStrip

logger = logging.getLogger('pyledserver.LEDStrip')
logger.setLevel(logging.DEBUG)

class LEDStrip(BaseStrip):
    def __init__(self, num, pin):
        # import HW interface library and initialize strip object
        from neopixel import Adafruit_NeoPixel, ws

        led_freq_hz    = 800000  # LED signal frequency in hertz (usually 800khz)
        led_dma        = 10      # DMA channel to use for generating signal (try 10)
        led_brightness = 255     # Set to 0 for darkest and 255 for brightest
        led_invert     = False   # True to invert the signal (when using NPN transistor level shift)
        led_channel    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        led_strip      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

        self.num_pixels = num

        self = Adafruit_NeoPixel(num,
                                 pin,
                                 led_freq_hz,
                                 led_dma,
                                 led_invert,
                                 led_brightness,
                                 led_channel,
                                 led_strip)