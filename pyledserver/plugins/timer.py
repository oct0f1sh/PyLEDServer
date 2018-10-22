import json
import logging
import threading
from time import sleep, time

logger = logging.getLogger('pyledserver.plugins.TimerThread')
logger.setLevel(logging.DEBUG)

class TimerThread(threading.Thread):
    """ visual timer """
    """ expected args:
    {
        "minutes": int,
        "seconds": int
    }
    """
    p_identifier = 'timer'
    p_name = 'Timer'
    p_author = 'oct0f1sh'
    p_expected_args = {'minutes': int, 'seconds': int}

    def __init__(self, led_strip, json_args):
        super(TimerThread, self).__init__()
        self.should_stop = False

        try:
            self.minutes = int(json_args['minutes'])
            self.seconds = int(json_args['seconds'])
        except (KeyError, ValueError) as err:
            logger.error('Invalid or missing minutes or seconds value')
            raise

        self.led_strip = led_strip

    def run(self):
        green = (0, 255, 0)
        red = (255, 0, 0)
        off = (0, 0, 0)

        self.led_strip.setStripColorRGB(*green)

        pixels = self.led_strip.num_pixels

        total_seconds = (self.minutes * 60) + self.seconds
        logger.debug('TOTAL SECONDS: {}'.format(total_seconds))

        leds_off = 0

        time_between_leds = float(total_seconds) / float(pixels)
        rec_time = time()

        # time measurement test stuff
        start_time = time()
        total_inaccuracy = 0.0
        ####

        while not self.should_stop:
            if (time() - rec_time) >= time_between_leds:
                overlap = (time() - rec_time) - time_between_leds

                total_inaccuracy += float(overlap)

                rec_time = time() - overlap

                self.led_strip.setPixelColorRGB((pixels - leds_off), *off)
                self.led_strip.show()

                if leds_off == pixels:
                    # logger.debug('Inaccuracy: {}'.format(total_inaccuracy))
                    logger.debug('Time elapsed: {:.4f} seconds, Inaccuracy: {:.4f} seconds'.format(float(time() - start_time), float(total_inaccuracy)))
                    break
                else:
                    leds_off += 1

        self.led_strip.setStripColorRGB(*red)