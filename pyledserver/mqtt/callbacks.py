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
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info('Successfully connected to MQTT server')
        else:
            logger.error('Failed to connect with rc: {}'.format(rc))

    def on_message(self, client, obj, msg):
        try:
            logger.debug('Checking if JSON')
            message = json.loads(msg.payload)
        except ValueError:
            logger.exception('Error processing message into JSON')
            return
        
        logger.info('Message received from topic: {}\n{}'.format(msg.topic, json.dumps(message, indent=4)))

    def on_publish(self, client, obj, mid):
        logger.debug('Message published.')

    def on_subscribe(self, client, obj, mid, granted_qos):
        logger.debug('Subscribed to topic')
