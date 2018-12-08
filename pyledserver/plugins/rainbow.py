import json
import logging
import threading
from time import sleep
from itertools import cycle

from colour import Color

logger = logging.getLogger('pyledserver.plugins.RainbowThread')
logger.setLevel(logging.INFO)

class RainbowThread(threading.Thread):
    """ Feedback to show that LED strip has been initialized successfully.
    Only called in client.py """
    """ expected args (there are none)
    {
        "start": {
            "r": int,
            "g": int,
            "b": int
        },
        "end": {
            "r": int,
            "g": int,
            "b": int
        },
        duration: int
    }
    """
    p_identifier = 'rainbow' # MUST NOT CONTAIN SPACES
    p_name = 'Rainbow'
    p_author = 'oct0f1sh'
    p_expected_args = {"duration": int}

    def __init__(self, led_strip, json_args):
        super(RainbowThread, self).__init__()
        self.should_stop = False

        try:
            self.duration = json_args['duration']
        except (KeyError, ValueError) as err:
            logger.error('Invalid JSON format')
            raise

        self.led_strip = led_strip

    def run(self):
        off = (0,0,0)

        rg = list(Color('red').range_to(Color('green'), self.led_strip.num_pixels))
        gb = list(Color('green').range_to(Color('blue'), self.led_strip.num_pixels))
        br = list(Color('blue').range_to(Color('red'), self.led_strip.num_pixels))

        colors = rg + gb + br

        iteration_length = self.duration / self.led_strip.num_pixels

        logger.debug('Iteration length: {}'.format(iteration_length))

        # for i, col in enumerate(cols):
        #     self.led_strip.setPixelColorRGB(i, *rgb)
        #     self.led_strip.show()

        #     sleep(iteration_length)
        i = 0

        for color in cycle(colors):
            self.led_strip.setPixelColorRGB(i, *color)

            if i == self.led_strip.num_pixels - 1:
                i = 0
            else:
                i += 1

            self.led_strip.show()


    # def minor_to_major(self, rgb):
    #     """ Change RGB value of range from 0 - 1 to 0 - 255 """
    #     return (rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)

    # def major_to_minor(self, rgb):
    #     return (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)