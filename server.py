#!python2

import paho.mqtt.client as mqtt
import os
import json
import sys
from mqtt_callback import CallbackContainer
from mqttinfo import MqttInfo

divider = '\n------------------'

try:
    from neopixel import Color
except ImportError:
    from debugColor import Color

if len(sys.argv) >= 1 and '--debug' not in sys.argv:
    print('NORMAL MODE' + divider)
    from LEDStrip import LEDStrip
    led_strip = LEDStrip(18, 60)
else:
    print('DEBUG MODE' + divider)
    from LEDStrip import DebugLEDStrip
    led_strip = DebugLEDStrip()

if __name__ == '__main__':
    user_info = MqttInfo()

    mqtt_host = user_info.mqtt_url
    mqtt_port = 10820

    mqtt_username = user_info.mqtt_username
    mqtt_password = user_info.mqtt_password

    # print('url: {}\nusername: {}\npassword: {}'.format(mqtt_host, mqtt_username, mqtt_password) + divider)
    print(divider[1:])

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