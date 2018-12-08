import logging

from strip.basestrip import BaseStrip

# logger = logging.getLogger('pyledserver.LEDStrip')
logger = logging.getLogger('pyledserver.strip.LEDStrip')
logger.setLevel(logging.DEBUG)

class LEDStrip(BaseStrip):
    # import HW interface library and initialize strip object
    # TODO: not too sure what I think of this import
    import neopixel
    import board

    def __init__(self, num, pin):
        self.led_pin = self.board.D18
        self.order = self.neopixel.GRB

        self.num_pixels = num

        self.strip = self.neopixel.NeoPixel(self.led_pin, self.num_pixels, brightness=1, auto_write=False, pixel_order=self.order)

        logger.debug('Setting LED strip')

        self.strip.fill((0,0,0))

    def setBrightness(self, brightness):
        self.strip = self.neopixel.NeoPixel(self.led_pin, self.num_pixels, brightness=brightness, auto_write=False, pixel_order=self.order)