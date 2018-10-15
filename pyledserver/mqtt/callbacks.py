import json
import logging
import threading

from utils.pluginmanager import PluginManager

logger = logging.getLogger('pyledserver.CallbackContainer')
logger.setLevel(logging.INFO)

class CallbackContainer(object):
    """ Manages MQTT callbacks """
    def __init__(self, led_strip):
        logger.debug('Initializing thread')
        self.thread = threading.Thread()
        self.led_strip = led_strip
        self.plugin_manager = PluginManager()
        self.is_connected = False
        
    def on_connect(self, client, userdata, flags, rc):
        self._evaluate_rc(rc)

    def on_disconnect(self, client, userdata, rc):
        self._evaluate_rc(rc)

    def _evaluate_rc(self, rc):
        if rc == 0: 
            logger.info('Successfully connected to MQTT server')
            self.is_connected = True
        elif rc == 1:
            logger.critical('Connection refused - incorrect protocol version')
            self.is_connected = False
        elif rc == 2:
            logger.critical('Connection refused - invalid client identifier')
            self.is_connected = False
        elif rc == 3:
            logger.critical('Connection refused - server unavailable')
            self.is_connected = False
        elif rc == 4:
            logger.critical('Connection refused - bad username or password')
            self.is_connected = False
        elif rc == 5:
            logger.critical('Connection refused - not authorized')
            self.is_connected = False
        else:
            logger.critical('Failed to connect with rc: {}'.format(rc))
            self.is_connected = False

    def _interpret_message(self, json):
        try:
            _ = json['message']
        except KeyError:
            logger.error('json missing message key')
            raise

        try:
            args = json['args']

            # all args keys must have a dictionary value
            if type(args) is not dict:
                raise KeyError('Args must be of type dictionary')
        except KeyError:
            logger.error('json missing args dictionary')
            raise
                
    def on_message(self, client, obj, msg):
        try:
            logger.debug('Checking if JSON')
            message = json.loads(msg.payload)
        except ValueError:
            logger.exception('Error processing message into JSON')
            return
        
        logger.info('Message received from topic: {}\n{}'.format(msg.topic, json.dumps(message, indent=4)))

        # check if json message adheres to proper structure
        try:
            self._interpret_message(message)
        except KeyError:
            # error is logged by logger in _interpret_message()
            return

        # if thread is already running
        if self.thread.isAlive():
            logger.info('Joining thread')
            # tell thread to stop and join it
            self.thread.should_stop = True
            self.thread.join()

        # seperate values into variables
        # this structure is validated in self._interpret_message()
        payload = message['message']
        args = message['args']

        # TODO: reset strip to blank slate

        # run plugin specified in message
        try:
            self.thread = self.plugin_manager.get_plugin_thread(payload, args, self.led_strip)
            self.thread.start()
        except (KeyError, ValueError):
            # this is executed when message does not correspond to an available plugin
            return

    def on_publish(self, client, obj, mid):
        logger.debug('Message published.')

    def on_subscribe(self, client, obj, mid, granted_qos):
        logger.debug('Subscribed to topic')
