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
    """ Manages MQTT callbacks """
    def __init__(self, led_strip):
        self.thread = threading.Thread()
        self.led_strip = led_strip
        self.plugin_manager = PluginManager()

    def on_connect(self, client, userdata, flags, rc):
        """ Displays result of connection attempt """
        if rc == 0:
            print('Successfully connected' + divider)
        else:
            print('Failed to connect with rc: {}'.format(rc) + divider)

    def on_message(self, client, obj, msg):
        """ Convert incoming messages to JSON and handle interpretation """
        try:
            message = json.loads(msg.payload)
        except ValueError as err:
            print('JSON ERROR: {}'.format(err) + divider)
            return

        print('Message received from topic: {}\n{}'.format(msg.topic, json.dumps(message, indent=4, separators=(',', ': '))))

        # check if json message adheres to proper structure
        try:
            self.interpret_message(message) 
        except KeyError:
            print(divider[1:])
            return
        
        print(divider[1:])

        # if previous thread is running then stop it and join it into main thread
        if self.thread.isAlive():
            print('JOINING THREAD' + divider)
            self.thread.should_stop = True
            self.thread.join()

        payload = message['message']
        args = message['args']

        # reset strip to a blank slate
        self.led_strip.wipe_strip()

        # run plugin specified in json message
        try:
            self.thread = self.plugin_manager.get_plugin_thread(payload, args, self.led_strip)
            self.thread.start()
        except (KeyError, ValueError):
            print(divider[1:])

    def interpret_message(self, json):
        """ Makes sure json adheres to proper structure """
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
        """ Display published messages """
        print('Message published.' + divider)

    def on_subscribe(self, client, obj, mid, granted_qos):
        """ Display subscribed topics """
        print('Subscribed to topic' + divider)