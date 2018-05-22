try:
    from neopixel import Color
except ImportError:
    from debugColor import Color
import json
import threading

class FillColorModule(object):
    def __init__(self, led_strip, json_args):
        try:
            r = int(json_args['r'])
            g = int(json_args['g'])
            b = int(json_args['b'])
        except ValueError:
            print('LEDSolidColorModule - INVALID RGB ARGUMENTS')
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

        self._set_solid()