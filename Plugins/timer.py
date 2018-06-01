try:
    from neopixel import Color
except ImportError:
    from debugColor import Color
import json
from time import sleep, time
import threading

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
    p_expected_args = {'minutes': 'int', 'seconds': 'int'}

    def __init__(self, led_strip, json_args):
        super(TimerThread, self).__init__()
        self.should_stop = False

        try:
            self.minutes = int(json_args['minutes'])
            self.seconds = int(json_args['seconds'])
        except (KeyError, ValueError) as err:
            print('TimerThread - INVALID MINUTES/SECONDS ARGUMENTS')
            raise

        self.led_strip = led_strip

    def run(self):
        self.led_strip.wipe_strip(Color(0, 255, 0))

        off = Color(0, 0, 0)

        pixels = self.led_strip.num_pixels

        total_seconds = (self.minutes * 60) + self.seconds

        print('TOTAL SECONDS: {}'.format(total_seconds))

        total_minutes = float(total_seconds) / 60.0

        print('TOTAL MINUTES: {}'.format(total_minutes))

        leds_off = 0

        time_between_leds = float(total_seconds) / float(pixels)
        rec_time = time()

        # time measurement test stuff
        start_time = time()
        ####

        while not self.should_stop:
            if (time() - rec_time) > time_between_leds:
                rec_time = time()

                self.led_strip.strip.setPixelColor((pixels - leds_off), off)
                self.led_strip.strip.show()

                if leds_off == pixels:
                    break
                else:
                    leds_off += 1

        print('TIME ELAPSED: {}'.format(time() - start_time))

        self.led_strip.wipe_strip(Color(255, 0, 0))