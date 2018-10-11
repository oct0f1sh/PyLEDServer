from utils.user import User
import json
import mqtt.callbacks as mqtt_util
import paho.mqtt.client as mqtt
import logging

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
    logger.info('Starting server')
    # get user credentials
    user = User()

    # create MQTT client and associate callbacks
    logger.debug('Creating client')
    client = mqtt.Client()
    callback = mqtt_util.CallbackContainer()
    client.on_message = callback.on_message
    client.on_publish = callback.on_publish
    client.on_subscribe = callback.on_subscribe

    # give user credentials to client
    client.username_pw_set(user.mqtt_username, user.mqtt_password)

    # connect to MQTT server and subscribe to topic
    logger.debug('Connecting to server {}:{}'.format(user.mqtt_url, user.mqtt_port))
    client.connect(user.mqtt_url, int(user.mqtt_port))
    client.subscribe('test', 0)

    success_message = {'message': 'successfully started client',
                       'args' : {}}

    # publish connection message to ensure successful connection
    client.publish('test', json.dumps(success_message, ensure_ascii=True))

    client.loop_forever()

# logging.exception() will show the traceback of what failed in a try; catch; except