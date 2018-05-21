try:
    from neopixel import Color
except ImportError:
    from debugColor import Color
import json

class LEDSolidColorModule(object):
    """ sets strip to one solid color """
    """ expected args:
        {
            'r': integer between 0, 255,
            'g': integer between 0, 255,
            'b': integer between 0, 255
        }
    """
    def __init__(self, led_strip, json_args):
        print(json_args)

        json_args = json.loads(json_args)

        # TODO: TRY / CATCH for non Int rgb arguments
        r = int(json_args['r'])
        g = int(json_args['g'])
        b = int(json_args['b'])

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

    def _set_solid(self):
        color = Color(self.r, self.g, self.b)

        self.led_strip.set_solid(color)