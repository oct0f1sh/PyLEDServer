from utils import user
import logging

logger = logging.getLogger('run')

def setup_logger():
    logger.setLevel(logging.DEBUG)

    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s', datefmt='%I:%M:%S')

    # ch.setFormatter(formatter)

    # logger.addHandler(ch)

if __name__ == "__main__":
    setup_logger()

    user = user.User()

    logger.info('nice')