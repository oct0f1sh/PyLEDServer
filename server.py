#!python3

# DO NOT RUN AS SUPERUSER

import paho.mqtt.client as mqtt
import os
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
    print('Message received from topic: {}\n\"{}\"'.format(msg.topic, message) + divider)

    if 'test strip' in message:
        led_strip.test_strip()

def on_publish(client, obj, mid):
    print('Message published.' + divider)

def on_subscribe(client, obj, mid, granted_qos):
    print('Subscribed to topic' + divider)

if __name__ == '__main__':
    mqtt_host = os.environ.get('MQTT_URL')
    mqtt_port = 10820

    mqtt_username = os.environ.get('MQTT_USERNAME')
    print(mqtt_username)
    mqtt_password = os.environ.get('MQTT_PASSWORD')
    print(mqtt_password)

    client = mqtt.Client()
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe

    client.username_pw_set(mqtt_username, mqtt_password)

    client.connect(mqtt_host, mqtt_port)
    client.subscribe('test', 0)

    client.publish('test', 'testing on topic: test')

    client.loop_forever()