"""
Training model for orthoTrack model
Author: npgh2009 & dentou
"""

import pygame, sys, random
from pygame.locals import *
from OrthogonalTrack import OrthogonalTrack, trackTemplate2
from Car import Car
from Sensor import SimpleFrontSensor
from neuralnet.feedForwardNeuralNet import NeuralNetwork

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Set game parameters
FPS = 60

# set up the window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Training Orthogonal Track')

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
#currCheckpoints = track.checkpoints[:]
#currCheckpointshitbox = track.checkpointshitbox[:]

# Set up cars parameters
x0_car = 70
y0_car = 75
CAR_WIDTH = 20
CAR_HEIGHT = 40

# Set up sensor parameters
SENSOR_RANGE = 100
RAY_SIZE = 1
SENSOR_ANGLE = 120
SENSOR_COUNT = 5

# Set up neural network parameters
NN_OUTPUT = 3 (Up, Left, Right)
NN_SIZE = [SENSOR_COUNT, 6, NN_OUTPUT]
THRESHOLD = 0.5 # Threshold for deciding whether to push button or not, choose by just passing SENSOR_RANGE into initial nn

# Initialize 10 instances of car, each instance is a dictionary with attribute
# 'car'
# 'sensor'
# 'nn' (Neural Network)
# 'cps' (Checkpoints)
# 'cpshb' (CheckpointsHitbox)
# 'move': A dictionary with 4 keys 'Up', 'Down', 'Left', 'Right'
# 'dead': Whether car is dead or not

CAR_COUNT = 10
cars = [{'car': Car(position=(x0_car, y0_car), direction=CAR_DIRECTION, size=(CAR_WIDTH, CAR_HEIGHT)),
			'sensor': None,
			'nn': NeuralNetwork(sizes = NN_SIZE),
			'cps': track.checkpoints[:],
			'cpshb': track.checkpointshitbox[:],
			'move': {'up': False,
					'down': False,
					'left': False,
					'right': False
					},
			'dead': False
			} for _ in range(CAR_COUNT)]

deadCount = 0
generation = 1

# Program loop
while True:
	# Get input event from user
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#exit window
			pygame.quit()
			sys.exit()

	# Read sensor value from each car, then feed through neuralnet, then output movement variables
	for i in range(CAR_COUNT):

		if cars[i]['dead']: #if car died, continue to next car
			continue

		else:
			# Initialize sensor, then read values (is there a way to prevent initialize each time)
			cars[i]['sensor'] = SimpleFrontSensor(car.model.topLeft, car.model.topRight,
										rnge = SENSOR_RANGE, angle = SENSOR_ANGLE, count = SENSOR_COUNT)
			cars[i]['sensor'].readSensor(track.walls)

			# Feed sensor value into neuralnet
			tempSensorValues = cars[i]['sensor'].outputValues() # 5x1 array
			nnOutputValues = cars[i]['nn'].feedForward(tempSensorValues) # 3x1 array -> Up, Left, Right
			nnOutputValues = nnOutputValues.flatten().tolist() # convert to list for easy manipulation

			# Turn on movement variables when value exceeds threshold
			upValue = nnOutputValues[0]
			if upValue > THRESHOLD:
				cars[i]['move']['up'] = True
				cars[i]['move']['down'] = False
			else:
				cars[i]['move']['up'] = False

			leftValue = nnOutputValues[1]
			if leftValue > THRESHOLD:
				cars[i]['move']['left'] = True
				cars[i]['move']['right'] = False
			else:
				cars[i]['move']['left'] = False

			rightValue = nnOutputValues[2]
			if rightValue > THRESHOLD:
				cars[i]['move']['right'] = True
				cars[i]['move']['left'] = False
			else:
				cars[i]['move']['right'] = False

			# Move the car
			if cars[i]['move']['up']:
				cars[i]['car'].accelerate(ACCELERATION)
			if cars[i]['move']['down']:
				cars[i]['car'].accelerate(-ACCELERATION)
			if cars[i]['car'].isMoving():
				if cars[i]['move']['left']:
					cars[i]['car'].turn(-TURN_SPEED / FPS)
				elif cars[i]['move']['right']:
					cars[i]['car'].turn(TURN_SPEED / FPS)
				if (not cars[i]['move']['left']) and (not cars[i]['move']['right']) and cars[i]['car'].isMoving():
					#car.brake(BRAKING_ACCELERATION)
					cars[i]['car'].accelerate(0)
			
			cars[i]['car'].update(1/FPS)

			# Check if car has intersected with any wall
			for wall in track.walls:
				if cars[i]['car'].isCollideWithRect(wall):
					cars[i]['dead'] = True
					deadCount += 1
					break

			# Check if car has interested with any checkpoint (may rewrite)
			for j, cp in enumerate(cars[i]['cps']):
				if cars[i]['car'].isCollideWithRect(cp):
					cars[i]['cps'].pop(j)
					cars[i]['cpshb'].pop(j)

	# Draw objects onto screen
	windowSurface.fill(BLACK)

	## Draw car

	## Draw walls

	## Draw texts

	# Check if all cars are dead
	if deadCount == CAR_COUNT:
		
		# Goes to next generation
		generation += 1


		# Update genes from geneCrossover and geneMutation

		# Reset car parameters


		pygame.time.wait(1000)

	# Draw the window onto the screen.
	pygame.display.update()
	mainClock.tick(FPS)

		