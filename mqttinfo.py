import os.path

divider = '\n------------------'

class MqttInfo(object):
    def __init__(self):
        if MqttInfo._is_first_time():
            f = open('user_info.txt', 'w')

            print('PLEASE INPUT REQUIRED INFORMATION')
            
            self.mqtt_url = raw_input('MQTT url: ')
            self.mqtt_username = raw_input('MQTT username: ')
            self.mqtt_password = raw_input('MQTT Password: ')

            f.writelines(['mqtt_url={}\n'.format(self.mqtt_url),
                'mqtt_username={}\n'.format(self.mqtt_username),
                'mqtt_password={}'.format(self.mqtt_password)])

            f.close()

        # read user stored info
        else:
            try:
                with open('user_info.txt', 'r') as f:
                    for line in f:
                        if '\#\#' not in line:
                            info = line.split('=')
                            if info[0] == 'mqtt_url':
                                self.mqtt_url = info[1][:-1]
                                print('url found')
                            elif info[0] == 'mqtt_username':
                                self.mqtt_username = info[1][:-1]
                                print('username found')
                            elif info[0] == 'mqtt_password':
                                self.mqtt_password = info[1][:-1]
                                print('password found')
            except IOError:
                print('CORRUPT OR INVALID user_info.txt')

    @staticmethod
    def _is_first_time():
        if os.path.isfile('user_info.txt'):
            return False
        else:
            return True