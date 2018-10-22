import json
import logging
import threading
from time import sleep

from colour import Color

logger = logging.getLogger('pyledserver.plugins.LEDSolidColorThread')
logger.setLevel(logging.DEBUG)

class WelcomeThread(threading.Thread):
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
    p_identifier = 'gradient' # MUST NOT CONTAIN SPACES
    p_name = 'Test LED functionality'
    p_author = 'oct0f1sh'
    p_expected_args = {"start": {"r": int, "g": int, "b": int}, "end": {"r": int, "g": int, "b": int}, "duration": int}

    def __init__(self, led_strip, json_args):
        super(WelcomeThread, self).__init__()

        try:
            self.start = Color(major)

        self.led_strip = led_strip
        self.should_stop = False

    def run(self):
        seconds = 2

        red = Color('red')
        green = Color(rgb=(0,1,0))
        off = (0,0,0)

        cols = list(red.range_to(green, self.led_strip.num_pixels))
        iteration_length = seconds / self.led_strip.num_pixels

        logger.debug('Iteration length: {}'.format(iteration_length))

        for i, col in enumerate(cols):
            rgb = self.minor_to_major(col.rgb)

            self.led_strip.setPixelColorRGB(i + 1, *rgb)

            sleep(iteration_length)

        for i, col in enumerate(cols):
            self.led_strip.setPixelColorRGB(i + 1, *off)

            sleep(iteration_length)

    def minor_to_major(self, rgb):
        """ Change RGB value of range from 0 - 1 to 0 - 255 """
        return (rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)

    def minor_to_major(self, rgb):
        return (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)