try:
    from neopixel import Color
except ImportError:
    from debugColor import Color
import json
from time import sleep
import threading

class MovingDotThread(threading.Thread):
    """ moves a dot back and fourth until cancelled """
    """ expected args:
        {
            'r': integer between 0, 255,
            'g': integer between 0, 255,
            'b': integer between 0, 255,
            'duration': integer
        }
    """
    p_identifier = 'ping_pong'
    p_name = 'Moving Dot'
    p_author = 'oct0f1sh'
    p_expected_args = {'r': 'int', 'g': 'int', 'b': 'int', 'duration': 'int'}

    def __init__(self, led_strip, json_args):
        super(MovingDotThread, self).__init__()
        self.should_stop = False

        try:
            r = int(json_args['r'])
            g = int(json_args['g'])
            b = int(json_args['b'])
        except (KeyError, ValueError) as err:
            print('MovingDotThread - INVALID RGB ARGUMENTS: {}'.format(err))
            raise

        try:
            self.duration = int(json_args['duration'])
        except (KeyError, ValueError) as err:
            print('MovingDotThread - INVALID DURATION VALUE')
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
        color = Color(self.r, self.g, self.b)
        off = Color(0, 0, 0)

        pixels = self.led_strip.num_pixels

        led_sleep_duration = float(self.duration) / float(pixels)

        i = 0
        forwards = True

        while not self.should_stop:
            if i == 0 and not forwards:
                self.led_strip.strip.setPixelColor(i + 1, off)
                self.led_strip.strip.setPixelColor(i, color)
                forwards = True
                i += 1
            elif i == pixels - 1:
                self.led_strip.strip.setPixelColor(i - 1, off)
                self.led_strip.strip.setPixelColor(i, color)
                forwards = False
                i -= 1
            else:
                if forwards:
                    self.led_strip.strip.setPixelColor(i - 1, off)
                    self.led_strip.strip.setPixelColor(i, color)
                    i += 1
                else:
                    self.led_strip.strip.setPixelColor(i + 1, off)
                    self.led_strip.strip.setPixelColor(i, color)
                    i -= 1

            self.led_strip.strip.show()
            sleep(led_sleep_duration)

    def no_run(self):
        num_points = 4

        bulge = []

        for i in reversed(range(1, num_points * 10, 10)):
            bulge.append(Color(self.r / i, self.g / i, self.b / i))

        bulge.extend(bulge[1::-1])

        for _ in range(self.led_strip.num_pixels - len(bulge)):
            bulge.append(Color(0, 0, 0))

        self.led_strip.set_pattern(bulge)