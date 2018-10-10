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