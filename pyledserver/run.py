from utils.user import User
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
    logger.info('Let\'s get you logged in...')
    user = User()



# logging.exception() will show the traceback of what failed in a try; catch; except