import logging

from strip.basestrip import BaseStrip

# logger = logging.getLogger('pyledserver.LEDStrip')
logger = logging.getLogger('pyledserver.strip.LEDStrip')
logger.setLevel(logging.DEBUG)

class LEDStrip(BaseStrip):
    def __init__(self, num, pin):
        # import HW interface library and initialize strip object
        import neopixel
        import board

        # led_freq_hz    = 800000  # LED signal frequency in hertz (usually 800khz)
        # led_dma        = 10      # DMA channel to use for generating signal (try 10)
        # led_brightness = 255     # Set to 0 for darkest and 255 for brightest
        # led_invert     = False   # True to invert the signal (when using NPN transistor level shift)
        # led_channel    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        # led_strip      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
        led_pin = board.D18
        order = neopixel.GRB

        self.num_pixels = num

        self = neopixel.NeoPixel(led_pin, self.num_pixels, brightness=1, auto_write=False, pixel_order=order)

        logger.debug('Setting LED strip')

        self.fill((255, 0, 0))
        self.show()

        # self.setPixelColorRGB(1, 255, 0, 0)