try:
    from neopixel import Color
except ImportError:
    from debugColor import Color
import json
from time import sleep
import threading

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
    p_expected_args = {'r': 'int', 'g': 'int', 'b': 'int', 'duration': 'int'}

    def __init__(self, led_strip, json_args):
        super(LEDSolidColorThread, self).__init__()
        self.should_stop = False

        try:
            r = int(json_args['r'])
            g = int(json_args['g'])
            b = int(json_args['b'])
        except ValueError as err:
            print('LEDSolidColorModule - INVALID RGB ARGUMENTS: {}'.format(err))
            raise

        try:
            self.duration = int(json_args['duration'])
        except (KeyError, ValueError) as err:
            print('LEDSolidColorModule - INVALID DURATION VALUE: {}'.format(err))

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
        color = Color(self.r, self.g, self.b)

        pixels = self.led_strip.num_pixels

        led_sleep_duration = float(self.duration) / float(pixels)

        for i in range(pixels):
            if self.should_stop:
                break

            self.led_strip.strip.setPixelColor(i, color)

            if self.duration != 0:
                sleep(led_sleep_duration)
            
            self.led_strip.strip.show()