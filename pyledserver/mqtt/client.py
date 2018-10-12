import json
import logging

import mqtt.callbacks as mqtt_util
import paho.mqtt.client as mqtt

logger = logging.getLogger('pyledserver.PyLEDClient')
logger.setLevel(logging.DEBUG)

class PyLEDClient(mqtt.Client):
    def __init__(self, client_id, credentials, mqtt_topic, led_strip):
        logger.debug('Creating client: {}'.format(client_id))

        # create and associate callbacks
        super().__init__(client_id=client_id, clean_session=False)
        self.callback = mqtt_util.CallbackContainer(led_strip)
        self.on_message = self.callback.on_message
        self.on_publish = self.callback.on_publish
        self.on_subscribe = self.callback.on_subscribe
        self.on_connect = self.callback.on_connect
        self.on_disconnect = self.callback.on_disconnect

        # assign user credentials to client
        self.username_pw_set(credentials.mqtt_username, credentials.mqtt_password)

        # connect to MQTT server and subscribe to topic
        logger.info('Connecting to server {}:{}'.format(credentials.mqtt_url, credentials.mqtt_port))
        self.connect(credentials.mqtt_url, int(credentials.mqtt_port))
        self.subscribe(mqtt_topic, 0)

        success = {'message': 'successfully started client',
                   'args': {}}

        # publish connection message to ensure successful connection
        self.publish(mqtt_topic, json.dumps(success, ensure_ascii=True))
    
    @property
    def is_connected(self):
        return self.callback.is_connected