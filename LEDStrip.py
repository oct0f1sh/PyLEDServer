#!python2

try:
    from neopixel import *
except ImportError:
    from debugColor import Color
import time
from PIL import ImageColor
from time import sleep

divider = '\n------------------'

class LEDStrip(object):
    def __init__(self, LED_PIN, LED_COUNT):
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

        self.num_pixels = self.strip.numPixels()

        self.strip.begin()

    def test_strip(self):
        strip = self.strip

        for i in range(self.num_pixels):
            if i % 3 == 0:
                color = Color(255, 0, 0)
            elif i % 3 == 1:
                color = Color(0, 255, 0)
            else:
                color = Color(0, 0, 255)

            strip.setPixelColor(i, color)

        strip.show()
        
    def wipe_strip(self, color=Color(0, 0, 0)):
        strip = self.strip

        for i in range(self.num_pixels):
            strip.setPixelColor(i, color)

        strip.show()

    def set_pattern(self, pattern):
        strip = self.strip

        for i in range(self.num_pixels):
            color = pattern[i % len(pattern)]

            print('Color: {}'.format(color))
            print('Index: {} Type: {}'.format(i, type(i)))
            strip.setPixelColor(i, color)

        strip.show()
        
class DebugStrip(object):
    def __init__(self):
        pass
    
    def setPixelColor(self, pixel, color):
        pass

    def show(self):
        pass

class DebugLEDStrip(object):
    def __init__(self):
        self.num_pixels = 60
        self.strip = DebugStrip()

    def test_strip(self):
        print('DEBUG MODE: testing LED strip' + divider)
    
    def wipe_strip(self, color):
        print('DEBUG MODE: setting strip to solid color: r:{} g:{} b:{}'.format(color.r, color.g, color.b) + divider)

if __name__ == '__main__':
    led_strip = LEDStrip(18, 60)