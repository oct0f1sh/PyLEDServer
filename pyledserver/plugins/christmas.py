import json
import logging
import threading
from time import sleep

logger = logging.getLogger('pyledserver.plugins.ChristmasThread')
logger.setLevel(logging.INFO)

class ChristmasThread(threading.Thread):
    """ red/green animation """
    """ expected args:
    {
        'duration': seconds between swap
    }
    """
    p_identifier = 'solid_color'
    p_name = 'Christmas Lights'
    p_author = 'oct0f1sh'
    p_expected_args = {'duration': int}

    def __init__(self, led_strip, json_args):
        super(ChristmasThread, self).__init__()
        self.should_stop = False

        try:
            self.duration = json_args['duration']
        except (KeyError, ValueError) as err:
            logger.error('Invalid JSON parameters')
            raise

        self.led_strip = led_strip

    def run(self):
        red = (255, 0, 0)
        green = (0, 255, 0)

        pixels = self.led_strip.num_pixels

        odd = False

        while not self.should_stop:
            for i in range(pixels):

                if i % 2 == 0:
                    self.led_strip.setPixelColor(i, green if odd else red)

            odd = not odd
                