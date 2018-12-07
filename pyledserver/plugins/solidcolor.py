import json
import logging
import threading
from time import sleep

logger = logging.getLogger('pyledserver.plugins.LEDSolidColorThread')
logger.setLevel(logging.DEBUG)

class LEDSolidColorThread(threading.Thread):
    """ sets strip to one solid color """
    """ expected args:
        {
            'r': integer between 0, 255,
            'g': integer between 0, 255,
            'b': integer between 0, 255,
            'duration': integer
        }
    """
    p_identifier = 'solid_color' # MUST NOT CONTAIN SPACES
    p_name = 'LED Solid Color'
    p_author = 'oct0f1sh'
    p_expected_args = {'r': int, 'g': int, 'b': int, 'duration': int}

    def __init__(self, led_strip, json_args):
        super(LEDSolidColorThread, self).__init__()
        self.should_stop = False

        try:
            r = int(json_args['r'])
            g = int(json_args['g'])
            b = int(json_args['b'])
        except (KeyError, ValueError) as err:
            logger.error('Invalid or missing RGB values'.format(err))
            raise

        try:
            self.duration = int(json_args['duration'])
        except (KeyError, ValueError) as err:
            logger.error('Invalid duration value')
            raise

        self.led_strip = led_strip
 
        # Check that all rgb values are less than 255
        if r < 256:
            self.r = r
        else:
            self.r = 0
        if g < 256:
            self.g = g
        else: 
            self.g = 0
        if b < 256:
            self.b = b
        else:
            self.b = 0

    def run(self):
        color = (self.r, self.g, self.b)

        pixels = self.led_strip.num_pixels

        led_sleep_duration = float(self.duration) / float(pixels)

        for i in range(pixels):
            if self.should_stop:
                break

            self.led_strip.setPixelColorRGB(i, *color)

            if self.duration != 0:
                self.led_strip.show()
                sleep(led_sleep_duration)
        
        if self.duration == 0:
            self.led_strip.show()
