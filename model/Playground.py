"""
Playground for testing models
Author: dentou
"""

import pygame
import sys

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Set game parameters
FPS = 60

# set up the window
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Playground')

# Set up the colors.
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# Draw the white background onto the surface.
	windowSurface.fill(WHITE)

	# Draw the window onto the screen.
	pygame.display.update()
	mainClock.tick(FPS)

