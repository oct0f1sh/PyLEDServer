import threading
import json

try:
    from neopixel import Color
except ImportError:
    from debugColor import Color

from Plugins import *
from pluginmanager import PluginManager

divider = '\n------------------'

class CallbackContainer(object):
    def __init__(self, led_strip):
        self.thread = threading.Thread()
        self.led_strip = led_strip
        self.plugin_manager = PluginManager()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print('Successfully connected' + divider)
        else:
            print('Failed to connect with rc: {}'.format(rc) + divider)

    def on_message(self, client, obj, msg):
        try:
            message = json.loads(msg.payload)
        except ValueError as err:
            print('JSON ERROR: {}'.format(err) + divider)
            return

        print('Message received from topic: {}\n{}'.format(msg.topic, json.dumps(message, indent=4, separators=(',', ': '))))

        try:
            self.interpret_message(message) 
        except KeyError:
            print(divider[1:])
            return
        
        print(divider[1:])

        if self.thread.isAlive():
            print('JOINING THREAD' + divider)
            self.thread.should_stop = True
            self.thread.join()

        payload = message['message']
        args = message['args']

        try:
            self.thread = self.plugin_manager.get_plugin_thread(payload, args, self.led_strip)
            self.thread.start()
        except ValueError:
            print(divider[1:])

        # if 'test strip' in payload:
        #     self.led_strip.test_strip()
        # if 'clear' in payload:
        #     self.led_strip.set_solid(Color(0, 0, 0))
        # if 'blue' in payload:
        #     self.led_strip.set_solid(Color(0, 0, 255))
        # if 'solid_color' in payload:
        #     try:
        #         self.thread = ledsolidcolorthread.LEDSolidColorThread(self.led_strip, args)
        #         self.thread.start()
        #     except ValueError:
        #         print(divider[1:])

    def interpret_message(self, json):
        try:
            _ = json['message']
        except KeyError:
            print('MISSING MESSAGE ARGUMENT IN JSON')
            raise
        try:
            args = json['args']

            if type(args) is not dict:
                raise KeyError('ARGS MUST BE OF TYPE DICTIONARY')
        except KeyError:
            print('MISSING DICTIONARY ARGS ARGUMENT IN JSON')
            raise
            

    def on_publish(self, client, obj, mid):
        print('Message published.' + divider)

    def on_subscribe(self, client, obj, mid, granted_qos):
        print('Subscribed to topic' + divider)