import argparse
import json
import logging
import sys

# This is needed to support Raspberry Pi Zero
sys.path.append('/home/pi/.local/lib/python3.5/site-packages')

from mqtt.client import PyLEDClient
from strip.ledstrip import LEDStrip
from strip.virtualstrip import VirtualStrip
from utils.credentials import CredentialsContainer

LED_COUNT = 60
LED_PIN = 18


def set_up_logger():
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
    # set up argument parser
    parser = argparse.ArgumentParser(description='Start PyLED server.')
    parser.add_argument('--debug', dest='is_debug', type=bool, const=True, nargs='?', default=False, help='Activate virtual LED strip.')
    # TODO: add argument for logging level with same level words like DEBUG or INFO
    # parser.add_argument(...)
    # parse arguments
    args = parser.parse_args()
    # log_levels = {'info': logging.INFO, 'debug': logging.DEBUG, ...}
    # log_level = log_levels[args.log_level]

    if args.is_debug:
        client_id = 'pyledserver_debug'
        led_strip = VirtualStrip(LED_COUNT)
    else:
        client_id = 'pyledserver_rpi'
        led_strip = LEDStrip(num=LED_COUNT, pin=LED_PIN)

    set_up_logger()

    # get user credentials
    user = CredentialsContainer()

    client = PyLEDClient(client_id, user, 'test', led_strip)

    # run the client
    # TODO: Find a better way to do this to auto reconnect
    client.loop_forever()
