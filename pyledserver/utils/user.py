import os.path
import logging

logger = logging.getLogger('run.user')

class User(object):
    def __init__(self):
        if User._is_first_setup():
            with open('user_info.txt', 'w') as f:
                self.mqtt_url      = input('MQTT url: ')
                self.mqtt_username = input('MQTT username: ')
                self.mqtt_password = input('MQTT password: ')
                self.mqtt_port     = input('MQTT port: ')

                f.writelines(['mqtt_url={}\n'.format(self.mqtt_url),
                              'mqtt_username={}\n'.format(self.mqtt_username),
                              'mqtt_password={}'.format(self.mqtt_password),
                              'mqtt_port={}'.format(self.mqtt_port)])

        else: # read stored user data
            try:
                with open('user_info.txt', 'r') as f:
                    for line in f:
                        if '\#\#' not in line: # if line is not a comment
                            info = line.split('=')
                            descriptor = info[0]
                            credential = info[1][:-1]

                            if descriptor == 'mqtt_url':
                                self.mqtt_url = credential
                                logging.info('URL found')
                            elif descriptor == 'mqtt_username':
                                self.mqtt_username = credential
                                logging.info('username found')
                            elif descriptor == 'mqtt_password':
                                self.mqtt_password = credential
                                logging.info('password found')
                            elif descriptor == 'mqtt_port':
                                self.mqtt_port = credential
                                logging.info('port found')
            except IOError:
                logger.error('Could not open user_info.txt')



    @staticmethod
    def _is_first_setup():
        if os.path.isfile('user_info.txt'): # checks for previous user_info.txt file
            logger.info('Found MQTT user credentials')
            return False

        logger.info('Performing first time setup')
        return True