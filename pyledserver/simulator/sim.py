import json
import logging
import sys

import pygame

logger = logging.getLogger('pyledserver.simulator.sim')
logger.setLevel(logging.DEBUG)

pygame.init()

# create display and set background to white
# TODO: Change display size based on number of LEDs
display = pygame.display.set_mode((1505, 30))
display.fill((255,255,255))
pygame.display.set_caption('LED Simulator')

clock = pygame.time.Clock()

# parameters for led sizes
led_rect_size = (20, 20)
led_rect_spacing = 25

def get_strip():
    """ Reads LED strip values from 'leds.json' file """
    logger.debug('Getting strip values')

    leds = {}

    with open('leds.json', 'r') as f:
        leds = json.load(f)

    return leds

def draw_leds():
    """ Saves LED strip values to 'leds.json' file """
    strip = get_strip()

    old_pos = (5,5)

    for pixel in strip["leds"]:
        color = (pixel['r'], pixel['g'], pixel['b'])
        black = (0, 0, 0)

        # draw filled pixel color
        pygame.draw.rect(display, color, [*old_pos, *led_rect_size])
        # draw pixel border (could there be a better way to do this?)
        # TODO: draw border and fill in one step
        pygame.draw.rect(display, black, [*old_pos, *led_rect_size], 2)

        # setup positioning for next pixel to be drawn
        old_pos = (old_pos[0] + led_rect_spacing, 5)

while True:
    # check for game exit thing? i guess this is something you're just supposed to do with pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    draw_leds()

    pygame.display.flip()
    clock.tick(60)
