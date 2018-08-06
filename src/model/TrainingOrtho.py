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
from neuralnet.geneCrossover import Crossover
from neuralnet.geneMutation import Mutation

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
CP_COUNT = len(track.checkpoints)

# Create current checkpoints list
#currCheckpoints = track.checkpoints[:]
#currCheckpointshitbox = track.checkpointshitbox[:]

# Set up cars parameters
x0_car = 70
y0_car = 75
CAR_WIDTH = 20
CAR_HEIGHT = 40
CAR_DIRECTION = (1,0)
ACCELERATION = 100
TURN_SPEED = 45

# Set up sensor parameters
SENSOR_RANGE = 100
RAY_SIZE = 1
SENSOR_ANGLE = 120
SENSOR_COUNT = 5

# Set up neural network parameters
NN_OUTPUT = 3 #(Up, Left, Right)
NN_SIZE = [SENSOR_COUNT, 6, NN_OUTPUT]
THRESHOLD = 0.15 # Threshold for deciding whether to push button or not, choose by just passing SENSOR_RANGE into initial nn

# Initialize 10 instances of car, each instance is a dictionary with attribute
# 'car'
# 'sensor'
# 'nn' (Neural Network)
# 'cps' (Checkpoints)
# 'cpshb' (CheckpointsHitbox)
# 'move': A dictionary with 4 keys 'Up', 'Down', 'Left', 'Right'
# 'dead': Whether car is dead or not

CAR_COUNT = 10 # should be greater than 2
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

# Initial generation value
deadCount = 0
generation = 1
genClock = 0
clockLimit = 300

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
			print("Car " + str(i) + " dead")
			continue

		else:
			print("Car " + str(i) + " not dead")
			# Initialize sensor, then read values (is there a way to prevent initialize each time)
			# (wonder if initialization will take time)
			cars[i]['sensor'] = SimpleFrontSensor(cars[i]['car'].model.topLeft, cars[i]['car'].model.topRight,
										rnge = SENSOR_RANGE, angle = SENSOR_ANGLE, count = SENSOR_COUNT)
			cars[i]['sensor'].readSensor(track.walls)

			# Feed sensor value into neuralnet
			tempSensorValues = cars[i]['sensor'].outputValues() # 5x1 array
			nnOutputValues = cars[i]['nn'].feedForward(tempSensorValues) # 3x1 array -> Up, Left, Right
			nnOutputValues = nnOutputValues.flatten().tolist() # convert to list for easy manipulation (maybe not necessary)

			# Turn on movement variables when value exceeds threshold
			upValue = nnOutputValues[0]
			if upValue > THRESHOLD:
				print("Car " + str(i) + " moving up")
				cars[i]['move']['up'] = True
				cars[i]['move']['down'] = False
			else:
				cars[i]['move']['up'] = False

			leftValue = nnOutputValues[1]
			if leftValue > THRESHOLD:
				print("Car " + str(i) + " moving left")
				cars[i]['move']['left'] = True
				cars[i]['move']['right'] = False
			else:
				cars[i]['move']['left'] = False

			rightValue = nnOutputValues[2]
			if rightValue > THRESHOLD:
				print("Car " + str(i) + " moving right")
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
					cars[i]['car'].accelerate(0)
			
			cars[i]['car'].update(1/FPS)

			# Check if car has intersected with any wall
			for wall in track.walls:
				if cars[i]['car'].isCollideWithRect(wall):
					print("Car " + str(i) + " has collided")
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
	for i in range(CAR_COUNT):
		if cars[i]['dead']:
			cars[i]['car'].draw(windowSurface, RED)
		else:
			cars[i]['car'].draw(windowSurface, WHITE)

	## Draw walls
	for i in range(len(track.walls)):
		pygame.draw.rect(windowSurface, GREEN, track.walls[i])

	## Draw texts
	### Set up fonts
	basicFont = pygame.font.SysFont(None, 24)
	### Set up texts
	genText = basicFont.render("Generation: " + str(generation), True, WHITE)
	genRect = genText.get_rect()
	genRect.topleft = (WINDOW_WIDTH - 275, 10)

	clockText = basicFont.render("Clock: " + str(genClock), True, WHITE)
	clockRect = clockText.get_rect()
	clockRect.topleft = (WINDOW_WIDTH - 275, 25)
	### Blit
	windowSurface.blit(genText, genRect)
	windowSurface.blit(clockText, clockRect)

	## Update game clock and display
	genClock += 1
	pygame.display.update()
	mainClock.tick(FPS)

	# Go to next generation if clock exceed limit
	if genClock > clockLimit:
		deadCount = CAR_COUNT

	# Check if all cars are dead
	if deadCount == CAR_COUNT:
		
		print("All cars dead")

		# Find two cars with the best fit
		cpsCount = list(enumerate([len(x['cps']) for x in cars]))
		cpsCount.sort(key = lambda x: x[1])
		print("Checkpoints count")
		print(cpsCount)
		firstGenes = cars[cpsCount[0][0]]['nn'].flattenWeights()
		secondGenes = cars[cpsCount[1][0]]['nn'].flattenWeights()

		# Update genes from geneCrossover and geneMutation
		for i in range(CAR_COUNT):
			crossover = Crossover(firstGenes, secondGenes, NN_SIZE)
			tempGenes = crossover.zigzag()
			mutation = Mutation(tempGenes, NN_SIZE)
			cars[i]['nn'].editGenes(mutation.gaussian(mu = 0, sigma = 0.2))

			# Reset car position
			cars[i]['car'].reset(position=(x0_car, y0_car), direction=CAR_DIRECTION, size=(CAR_WIDTH, CAR_HEIGHT))

			# Reset car status
			cars[i]['dead'] = False
			cars[i]['cps'] = track.checkpoints[:]
			cars[i]['cpshb'] = track.checkpointshitbox[:]
			cars[i]['move'] = {'up': False,
					'down': False,
					'left': False,
					'right': False}

		# Goes to next generation
		generation += 1
		deadCount = 0
		genClock = 0
		clockLimit += 100

		# Delay game before going to next generation
		pygame.time.wait(1000)