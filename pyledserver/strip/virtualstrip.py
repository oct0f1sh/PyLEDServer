import json
import logging
import subprocess
import sys
import os

from strip.basestrip import BaseStrip

logger = logging.getLogger('pyledserver.VirtualStrip')
logger.setLevel(logging.INFO)

class VirtualStrip(BaseStrip):
    def __init__(self, num):
        logger.info('Initialized virtual LED strip')

        self.num_pixels = num

        # self.leds = self.create_empty_led_dict()
        # make it clean that it has a return value
        self._initialize_empty_strip()

        subprocess.Popen(['python', '{}/simulator/sim.py'.format(os.getcwd())])

    def setPixelColorRGB(self, n, r, g, b):
        logger.debug('Setting pixel color')

        leds = self.get_strip()

        leds["leds"][n - 1] = {"r": r, "g": g, "b": b}

        self.set_strip(leds)

    def get_strip(self):
        logger.debug('Getting strip values')

        leds = {}

        with open('leds.json', 'r') as f:
            leds = json.load(f)

        return leds

    def set_strip(self, leds):
        logger.debug('Setting strip values')

        with open('leds.json', 'w') as f:
            f.write(json.dumps(leds, indent=4))

    def _initialize_empty_strip(self):
        logger.debug('Initializing empty strip file')

        json_leds = {"leds": []}
        """ JSON structure:
        {
            "leds": [
                {"r": 0, "g": 0, "b": 0},
                {"r": 0, "g": 0, "b": 0},
                ...
            ]
        }
        """

        for _ in range(self.num_pixels):
            json_leds["leds"].append({"r": 0, "g": 0, "b": 0})

        with open('leds.json', 'w') as f:
            f.write(json.dumps(json_leds))

if __name__ == '__main__':
    strip = VirtualStrip(60)
    strip.setPixelColorRGB(1, 255, 0, 0)
    strip.setPixelColorRGB(2, 0, 255, 0)
    strip.setPixelColorRGB(3, 0, 0, 255)
    strip.setPixelColorRGB(4, 255, 255, 255)
    # strip.thread.start()
