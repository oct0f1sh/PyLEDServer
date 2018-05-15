#!python2

import paho.mqtt.client as mqtt
import os
import json
from neopixel import Color
from LEDStrip import LEDStrip

divider = '\n------------------'

led_strip = LEDStrip(18, 60)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Successfully connected' + divider)
    else:
        print('Failed to connect with rc: {}'.format(rc) + divider)

def on_message(client, obj, msg):
    message = msg.payload.decode("utf-8")

    try:
        message = json.loads(message)

        print(message + divider)
        print(message['message'])
    except ValueError:
        print('MISSING DELIMITER IN JSON')

    print('Message received from topic: {}\n\"{}\"'.format(msg.topic, message) + divider)

    if 'test strip' in message:
        led_strip.test_strip()
    if 'clear' in message:
        led_strip.set_solid(Color(0, 0, 0))
    if 'blue' in message:
        led_strip.set_solid(Color(0, 0, 255))

def on_publish(client, obj, mid):
    print('Message published.' + divider)

def on_subscribe(client, obj, mid, granted_qos):
    print('Subscribed to topic' + divider)

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
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe

    client.username_pw_set(mqtt_username, mqtt_password)

    client.connect(mqtt_host, mqtt_port)
    client.subscribe('test', 0)

    client.publish('test', 'testing on topic: test')

    client.loop_forever()