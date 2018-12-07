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
        self.should_stop = False

        try:
            start_json = json_args['start']
            start_r = start_json['r']
            start_g = start_json['g']
            start_b = start_json['b']
            self.start_color = Color(rgb=(self.major_to_minor((start_r, start_g, start_b))))

            end_json = json_args['end']
            end_r = end_json['r']
            end_g = end_json['g']
            end_b = end_json['b']
            self.end_color = Color(rgb=(self.major_to_minor((end_r, end_g, end_b))))
        except (KeyError, ValueError) as err:
            logger.error('Invalid or missing start/end RGB values')

        self.led_strip = led_strip

    def run(self):
        seconds = 2

        off = (0,0,0)

        cols = list(self.start_color.range_to(self.end_color, self.led_strip.num_pixels))
        iteration_length = seconds / self.led_strip.num_pixels

        logger.debug('Iteration length: {}'.format(iteration_length))

        for i, col in enumerate(cols):
            rgb = self.minor_to_major(col.rgb)

            self.led_strip.setPixelColorRGB(i, *rgb)
            self.led_strip.show()

            sleep(iteration_length)

        for i, col in enumerate(cols):
            self.led_strip.setPixelColorRGB(i, *off)
            self.led_strip.show()

            sleep(iteration_length)

    def minor_to_major(self, rgb):
        """ Change RGB value of range from 0 - 1 to 0 - 255 """
        return (rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)

    def major_to_minor(self, rgb):
        return (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)