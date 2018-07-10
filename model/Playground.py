"""
Playground for testing models
Author: dentou
"""

import pygame
import sys
from model.Car import Car

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Playground')



# Set up the colors.
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)



# Setup car
car = Car((300, 300))

# Set up movement variables.
moveUp = False
moveDown = False
moveLeft = False
moveRight = False

MOVESPEED = 4

FPS = 60

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			# Change the keyboard variables.
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				moveRight = False
				moveLeft = True
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				moveLeft = False
				moveRight = True
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				moveDown = False
				moveUp = True
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				moveUp = False
				moveDown = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				moveLeft = False
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				moveRight = False
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				moveUp = False
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				moveDown = False


	# Move the car
	if moveUp:
		car.accelerate(100)
	if moveDown:
		car.accelerate(-100)
	if car.is_moving():
		if moveLeft:
			car.turn(30/FPS) # 30 degrees per second
		elif moveRight:
			car.turn(-30/FPS)
		if (not moveUp) and (not moveDown) and car.is_moving():
			car.brake()

	car.update(1/FPS)



	# Draw the white background onto the surface.
	windowSurface.fill(WHITE)

	# Draw the player onto the surface.
	#pygame.draw.rect(windowSurface, BLACK, player)

	# Draw car
	car.draw(windowSurface, BLACK)

	# Draw the window onto the screen.
	pygame.display.update()
	mainClock.tick(FPS)

