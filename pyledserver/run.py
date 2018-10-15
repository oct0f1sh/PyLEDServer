import json
import logging
import argparse

from strip.ledstrip import LEDStrip
from utils.credentials import CredentialsContainer
from mqtt.client import PyLEDClient

LED_COUNT = 60
LED_PIN = 18

# parse arguments
parser = argparse.ArgumentParser(description='Start PyLED server.')
parser.add_argument('--debug', dest='is_debug', type=bool, const=True, nargs='?', default=False, help='Activate virtual LED strip.')
is_debug = parser.parse_args().is_debug

# create logger
logger = logging.getLogger('pyledserver')
logger.setLevel(logging.DEBUG)

# create file handler for logging
fh = logging.FileHandler('pyledserver.log')
fh.setLevel(logging.DEBUG)

# create console logger
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create logger formatter
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s', datefmt='%I:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add handlers to logger
logger.addHandler(fh)
logger.addHandler(ch)

if __name__ == "__main__":
    if is_debug:
        client_id = 'pyledserver_debug'
        led_strip = LEDStrip(num=LED_COUNT, pin=None)
    else:
        client_id = 'pyledserver_rpi'
        led_strip = LEDStrip(num=LED_COUNT, pin=LED_PIN)

    # get user credentials
    user = CredentialsContainer()

    client = PyLEDClient(client_id, user, 'test', led_strip)

    # run the client
    # TODO: Find a better way to do this to auto reconnect
    client.loop_forever()