"""
Playground for orthoTrack model
Author: npgh2009 & dentou
"""

import pygame, sys, random
from pygame.locals import *
from OrthogonalTrack import OrthogonalTrack, trackTemplate2
from Car import Car
from Sensor import SimpleFrontSensor

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Set game parameters
FPS = 60

# set up the window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Playground Orthogonal Track')

# Set up the colors.
BLACK  = (0, 0, 0)
GREEN  = (0, 255, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 128, 0)

# Set up direction
UP = 8
DOWN = 2
LEFT = 4
RIGHT = 6

#Setup track
x0_track = 50
y0_track = 50
track = trackTemplate2(x0_track, y0_track)

# Create current checkpoints list
currCheckpoints = track.checkpoints[:]
currCheckpointshitbox = track.checkpointshitbox[:]

# Setup car
ACCELERATION = 100 # pixels per second squared
					# final speed will be ACCELERATION / DRAG_COEFF
BRAKING_ACCELERATION = 300
TURN_SPEED = 45 # degrees per second
CAR_DIRECTION = (1,0)

x0_car = 70
y0_car = 75

CAR_WIDTH = 20
CAR_HEIGHT = 40
car = Car(position=(x0_car, y0_car), direction=CAR_DIRECTION, size=(CAR_WIDTH, CAR_HEIGHT))

# Set up movement variables.
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
brake = False

# Set up sensor variable
SENSOR_RANGE = 100
RAY_SIZE = 1
SENSOR_ANGLE = 120
SENSOR_COUNT = 5

# Game loop
while True:
	#get input event from user
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#exit window
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
				#car.brake(BRAKING_ACCELERATION)
				car.accelerate(0)
				pass

	car.update(1 / FPS)

	# If car goes out of window, reset
	if ((car.model.topLeft.x < 0) or (car.model.topRight.x < 0) or (car.model.bottomLeft.x < 0) or (
			car.model.bottomRight.x < 0) or
			(car.model.topLeft.x > WINDOW_WIDTH) or (car.model.topRight.x > WINDOW_WIDTH) or (
					car.model.bottomLeft.x > WINDOW_WIDTH) or
			(car.model.bottomRight.x > WINDOW_WIDTH) or
			(car.model.topLeft.y < 0) or (car.model.topRight.y < 0) or (car.model.bottomLeft.y < 0) or (
					car.model.bottomRight.y < 0) or
			(car.model.topLeft.y > WINDOW_HEIGHT) or (car.model.topRight.y > WINDOW_HEIGHT) or (
					car.model.bottomLeft.y > WINDOW_HEIGHT) or
			(car.model.bottomRight.y > WINDOW_HEIGHT)):
		car.reset(position=(x0_car, y0_car), direction=CAR_DIRECTION, size=(CAR_WIDTH, CAR_HEIGHT)) #reset car to original position 

	# Draw the white background onto the surface.
	windowSurface.fill(BLACK)

	# Draw car
	car.draw(windowSurface, WHITE)

	# Create sensor for car
	carSensor = SimpleFrontSensor(car.model.topLeft, car.model.topRight, rnge = SENSOR_RANGE, angle = SENSOR_ANGLE, count = SENSOR_COUNT)
	carSensor.readSensor(track.walls)

	# Draw sensor
	for sensor in carSensor.sensorList:
		if sensor['dist'] < SENSOR_RANGE:
			pygame.draw.line(windowSurface, RED, sensor['pos'].asTuple(), carSensor.MiddleFront.asTuple(), RAY_SIZE)
		else:
			pygame.draw.line(windowSurface, YELLOW, sensor['pos'].asTuple(), carSensor.MiddleFront.asTuple(), RAY_SIZE)

    # check if car has intersected with any wall
	for i, wall in enumerate(track.walls):
		if car.isCollideWithRect(wall):
			car.reset(position=(x0_car, y0_car), direction=CAR_DIRECTION, size=(CAR_WIDTH, CAR_HEIGHT)) #reset car to original position
			currCheckpoints = track.checkpoints[:] #reset checkpoints
			currCheckpointshitbox = track.checkpointshitbox[:]
			car.draw(windowSurface, RED) #not working, why?
			pygame.time.wait(200)
			break

   	# check if car has interested with any checkpoint (may rewrite)
	for i, cp in enumerate(currCheckpointshitbox):
		if car.isCollideWithRect(cp):
			currCheckpoints.pop(i)
			currCheckpointshitbox.pop(i)

    # Draw walls and checkpoints
	for i in range(len(track.walls)):
		pygame.draw.rect(windowSurface, GREEN, track.walls[i])
	for i in range(len(currCheckpoints)):
		pygame.draw.rect(windowSurface, BLUE, currCheckpoints[i])


	# Draw the window onto the screen.
	pygame.display.update()
	mainClock.tick(FPS)
