"""
Playground for testing models
Author: dentou
"""

import pygame
import sys
from Point import Point
from Track import Track
from Car import Car

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Set game parameters
FPS = 60

# set up the window
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Playground')

# Set up the colors.
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Set up track
pointList = [Point(100, 100), Point(400, 100), Point(200, 400), Point(500, 500)]
widthMap = dict()
widthMap[pointList[0]] = 100
widthMap[pointList[1]] = 75
widthMap[pointList[2]] = 120
track = Track(pointList, widthMap, screen, BLACK, 2, 7)
track.generateBorderPoints()
print(track.centerPoints)
print(track.leftBorderPoints)
print(track.rightBorderPoints)

# Setup car
x0 = 75
y0 = 75
CAR_WIDTH = 20
CAR_HEIGHT = 40
car = Car(position=(x0, y0), direction=(1,0), size=(CAR_WIDTH, CAR_HEIGHT))
# Set speed parameters
ACCELERATION = 100 # pixels per second squared
				# final speed will be ACCELERATION / DRAG_COEFF
BRAKING_ACCELERATION = 300
TURN_SPEED = 45 # degrees per second
# Choose whether to set car when going out of window
CAR_RESET = True
# Set up movement variables.
moveUp = False
moveDown = False
moveLeft = False
moveRight = False

brake = False



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
			if event.key == pygame.K_SPACE:
				brake = True

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
			if event.key == pygame.K_SPACE:
				brake = False

	# Move the car
	if brake:
		car.brake(BRAKING_ACCELERATION)
	else:
		if moveUp:
			car.accelerate(ACCELERATION)
		if moveDown:
			car.accelerate(-ACCELERATION)
		if car.isMoving():
			if moveLeft:
				car.turn(-TURN_SPEED / FPS)
			elif moveRight:
				car.turn(TURN_SPEED / FPS)
			if (not moveUp) and (not moveDown) and car.isMoving():
				# car.brake(BRAKING_ACCELERATION)
				car.accelerate(0)
				pass

	car.update(1 / FPS)

	if car.isCollidedWithTrack(track):
		print("Collided")
		car.reset(position=(x0, y0), direction=(1,0), size=(CAR_WIDTH, CAR_HEIGHT))

	# Draw the white background onto the surface.
	screen.fill(WHITE)

	# Draw track
	track.draw()

	# Draw car
	car.draw(screen, BLUE)

	# Draw the window onto the screen.
	pygame.display.update()
	mainClock.tick(FPS)

