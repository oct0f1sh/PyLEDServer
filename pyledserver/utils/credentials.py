import os.path
import logging

logger = logging.getLogger('pyledserver.User')
logger.setLevel(logging.DEBUG)

class CredentialsContainer(object):
    def __init__(self):
        if CredentialsContainer._is_first_setup():
            with open('user_info.txt', 'w') as f:
                self.mqtt_url      = input('MQTT url: ')
                self.mqtt_username = input('MQTT username: ')
                self.mqtt_password = input('MQTT password: ')
                self.mqtt_port     = input('MQTT port: ')

                f.writelines(['mqtt_url={}\n'.format(self.mqtt_url),
                              'mqtt_username={}\n'.format(self.mqtt_username),
                              'mqtt_password={}\n'.format(self.mqtt_password),
                              'mqtt_port={}'.format(self.mqtt_port)])

        # read stored user data
        else: 
            logger.debug('Not first time setup')
            try:
                logger.debug('Trying to open file')
                with open('user_info.txt', 'r') as f:
                    logger.debug('Opened file')

                    for line in f:
                        # if line is not a comment
                        if '\#\#' not in line and line.isprintable: 
                            info = line.split('=')

                            try:
                                descriptor = info[0]
                                credential = info[1][:-1]
                            except IndexError as err:
                                logger.error('Error parsing credentials: {}'.format(err))
                                logger.error(info)

                            if descriptor == 'mqtt_url':
                                self.mqtt_url = credential
                                logger.debug('URL found')
                            elif descriptor == 'mqtt_username':
                                self.mqtt_username = credential
                                logger.debug('username found')
                            elif descriptor == 'mqtt_password':
                                self.mqtt_password = credential
                                logger.debug('password found')
                            elif descriptor == 'mqtt_port':
                                self.mqtt_port = credential
                                logger.debug('port found')

                    # validate that all credentials were found
                    # TODO: This doesn't actually work, so make it work
                    # if self.mqtt_url:
                    #     logger.error('Missing mqtt_url in user_info.txt')
                    # if self.mqtt_username:
                    #     logger.error('Missing mqtt_username in user_info.txt')
                    # if self.mqtt_password:
                    #     logger.error('Missing mqtt_password in user_info.txt')
                    # if self.mqtt_port:
                    #     logger.error('Missing mqtt_port in user_info.txt')

            except IOError:
                logger.exception('Could not open user_info.txt')


    @staticmethod
    def _is_first_setup():
        if os.path.isfile('user_info.txt'): # checks for existing user_info.txt file in current directory
            logger.info('Found MQTT user credentials')
            return False

        logger.info('Performing first time setup')
        return True