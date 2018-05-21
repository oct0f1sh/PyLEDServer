#!python2

import paho.mqtt.client as mqtt
import os
import json
from neopixel import Color
from LEDStrip import LEDStrip

from ledsolidcolormodule import LEDSolidColorModule

divider = '\n------------------'

led_strip = LEDStrip(18, 60)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Successfully connected' + divider)
    else:
        print('Failed to connect with rc: {}'.format(rc) + divider)

def on_message(client, obj, msg):
    try:
        message = json.loads(msg.payload)
    except ValueError as err:
        print('JSON ERROR: {}'.format(err) + divider)
        return

    print('Message received from topic: {}\n{}'.format(msg.topic, json.dumps(message, indent=4, separators=(',', ': '))))

    try:
        interpret_message(message) 
    except KeyError:
        print(divider)
        return
    
    print(divider)

    payload = message['message']
    args = message['args']

    if 'test strip' in payload:
        led_strip.test_strip()
    if 'clear' in payload:
        led_strip.set_solid(Color(0, 0, 0))
    if 'blue' in payload:
        led_strip.set_solid(Color(0, 0, 255))
    if 'solid_color' in payload:
        LEDSolidColorModule(led_strip, args)

def interpret_message(json):
    try:
        _ = json['message']
    except KeyError:
        print('MISSING MESSAGE ARGUMENT IN JSON')
        raise
    try:
        _ = json['args']
    except KeyError:
        print('MISSING ARGS ARGUMENT IN JSON')
        raise
        

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

    success_message = {'message': 'successfully started client'}

    client.publish('test', json.dumps(success_message, ensure_ascii=True))

    client.loop_forever()