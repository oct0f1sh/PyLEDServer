#!python2

import paho.mqtt.client as mqtt
import os
import json
import sys
from mqtt_callback_container import CallbackContainer

divider = '\n------------------'

try:
    from neopixel import Color
except ImportError:
    from debugColor import Color

from ledsolidcolormodule import LEDSolidColorModule

if len(sys.argv) >= 1 and '--debug' not in sys.argv:
    print('NORMAL MODE' + divider)
    from LEDStrip import LEDStrip
    led_strip = LEDStrip(18, 60)
else:
    print('DEBUG MODE' + divider)
    from LEDStrip import DebugLEDStrip
    led_strip = DebugLEDStrip()

class MqttInfo(object):
    def __init__(self):
        with open('user_info.txt', 'r') as f:
            for line in f:
                if '\#\#' not in line:
                    info = line.split('=')
                    if info[0] == 'mqtt_url':
                        self.mqtt_url = info[1][:-1]
                    elif info[0] == 'mqtt_username':
                        self.mqtt_username = info[1][:-1]
                    elif info[0] == 'mqtt_password':
                        self.mqtt_password = info[1][:-1]

if __name__ == '__main__':
    user_info = MqttInfo()

    mqtt_host = user_info.mqtt_url
    mqtt_port = 10820

    mqtt_username = user_info.mqtt_username
    mqtt_password = user_info.mqtt_password

    print('url: {}\nusername: {}\npassword: {}'.format(mqtt_host, mqtt_username, mqtt_password) + divider)

    client = mqtt.Client()
    callback = CallbackContainer(led_strip)
    client.on_message = callback.on_message
    client.on_publish = callback.on_publish
    client.on_subscribe = callback.on_subscribe

    client.username_pw_set(mqtt_username, mqtt_password)

    client.connect(mqtt_host, mqtt_port)
    client.subscribe('test', 0)

    success_message = {'message': 'successfully started client',
                       'args': {}}

    client.publish('test', json.dumps(success_message, ensure_ascii=True))

    client.loop_forever()