# dummy version of https://github.com/jgarff/rpi_ws281x/blob/master/python/neopixel.py

import logging

logger = logging.getLogger('pyledserver.BaseStrip')
logger.setLevel(logging.INFO)

class BaseStrip(object):
    def __init__(self, num, pin, freq_hz=None, dma=None, invert=None, brightness=None, channel=None, strip_type=None):
        logger.info('Initialized dummy strip')
        
        self.num_pixels = num
        self.pin = pin

    def _cleanup(self):
        logger.debug('_cleanup method')

    def begin(self):
        logger.debug('begin method')

    def show(self):
        logger.debug('show method')

    def setPixelColor(self, n, color):
        logger.debug('setPixelColor method')

    def setPixelColorRGB(self, n, red, green, blue, white=0):
        logger.debug('setPixelColorRGB method')

    def setBrightness(self, brightness):
        logger.debug('setBrightness method')

    def getBrightness(self):
        logger.debug('getBrightness method')

    def getPixels(self):
        logger.debug('getPixels method')

    def numPixels(self):
        logger.debug('numPixels method')

    def getPixelColor(self, n):
        logger.debug('getPixelColor method')