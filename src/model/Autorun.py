"""
Autorun script
Author: npgh2009 & dentou
"""

import pygame, sys, random
from pygame.locals import *
from Car import Car
from utils.AccelerationGenerator import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Autorun')

# Set up the colors.
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Setup car
x0 = 300
y0 = 500
CARWIDTH = 20
CARHEIGHT = 40
car = Car(position = (x0, y0), size = (CARWIDTH, CARHEIGHT))

# Set up movement variables.
moveUp = False
moveDown = False
moveLeft = False
moveRight = False

# Acceleration & turnspeed
acce = AccelerationGenerator(start = 0)
tusp = TurnspeedGenerator(start = 0)
BRAKE = 100
CARRESET = True

FPS = 60

# Set condition for acceleration to happen:
MINACCE = 5

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# Get acceleration & turnspeed
	acce.periodic(incre = 35)
	tusp.zigzag(duration = FPS)

	# Get move direction
	print('Acceleration value: '+str(acce.value))
	if acce.value > MINACCE:
		print('Acceleration larger than '+str(MINACCE)+'. Car is accelerating.')
		moveUp = True
	else:
		print('Car is not accelerating')
		moveUp = False
	print('Turnspeed value: '+str(tusp.value))
	if tusp.value > 0:
		print('Turning left')
		moveLeft = True
		moveRight = False
	else:
		print('Turning right')
		moveLeft = False
		moveRight = True

	# Move the car
	if moveUp:
		car.accelerate(acce.value)
	if moveDown:
		car.accelerate(-acce.value)
	if car.isMoving():
		if moveLeft:
			car.turn(tusp.value/FPS) # 30 degrees per second
		elif moveRight:
			car.turn(tusp.value/FPS)
		if (not moveUp) and (not moveDown) and car.isMoving():
			pass

	car.update(1/FPS)

	# If car goes out of window, reset
	if CARRESET:
		if ((car.model.topLeft.x < 0) or (car.model.topRight.x < 0) or (car.model.bottomLeft.x < 0) or (car.model.bottomRight.x < 0) or
			(car.model.topLeft.x > WINDOWWIDTH) or (car.model.topRight.x > WINDOWWIDTH) or (car.model.bottomLeft.x > WINDOWWIDTH) or
			(car.model.bottomRight.x > WINDOWWIDTH) or
			(car.model.topLeft.y < 0) or (car.model.topRight.y < 0) or (car.model.bottomLeft.y < 0) or (car.model.bottomRight.y < 0) or
			(car.model.topLeft.y > WINDOWHEIGHT) or (car.model.topRight.y > WINDOWHEIGHT) or (car.model.bottomLeft.y > WINDOWHEIGHT) or
			(car.model.bottomRight.y > WINDOWHEIGHT)):
			car.reset(position = (x0, y0), size = (CARWIDTH, CARHEIGHT))

	# Draw the white background onto the surface.
	windowSurface.fill(WHITE)

	# Draw cars
	car.draw(windowSurface, BLACK)

	# Draw the window onto the screen.
	pygame.display.update()
	mainClock.tick(FPS)