import sys

import logging
import pygame
from basestrip import BaseStrip
import threading
import time

logger = logging.getLogger('pyledserver.VirtualStrip')
logger.setLevel(logging.DEBUG)

# pygame.init()

# display = pygame.display.set_mode((1000, 200))
# pygame.display.set_caption('Swag money')

# should_quit = False

# clock = pygame.time.Clock()

# while not should_quit:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()

#     pygame.draw.rect(display, (255, 0, 0), (0, 0, 200, 200))

#     pygame.display.flip()
#     clock.tick(60)

class VirtualStrip(BaseStrip):
    def __init__(self, num):
        logger.info('Initialized virtual LED strip')

        self.thread = threading.Thread(target=self._run_simulator)
    
    def _setup_simulator(self):
        pygame.init()
        resolution = (1000, 50)

        self.display = pygame.display.set_mode(resolution)
        pygame.display.set_caption('PyLEDServer Simulator')

    def _run_simulator(self):
        self._setup_simulator()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            pygame.display.flip()

    def show(self):
        print('skunk')
        pygame.display.set_caption('swag money')


if __name__ == '__main__':
    strip = VirtualStrip(60)

    strip.thread.start()