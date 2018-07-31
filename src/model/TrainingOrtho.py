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
NN_SIZE = [SENSOR_COUNT, 6, 3]

# Initialize 20 instances of "individual", each instance is a dictionary with attribute
# 'car'
# 'sensor'
# 'nn' (Neural Network)
# 'cps' (Checkpoints)
# 'cpshb' (CheckpointsHitbox)
# 'move': A dictionary with 4 keys 'Up', 'Down', 'Left', 'Right'
cars = [{'car': Car(position=(x0_car, y0_car), direction=CAR_DIRECTION, size=(CAR_WIDTH, CAR_HEIGHT)),
			'sensor': None,
			'nn': NeuralNetwork(sizes = NN_SIZE),
			'cps': track.checkpoints[:],
			'cpshb': track.checkpointshitbox[:],
			'move': {'Up': False,
					'Down': False,
					'Left': False,
					'Right': False
					}
			} for _ in range(20)]

# Program loop
while True:
	# Get input event from user
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#exit window
			pygame.quit()
			sys.exit()

	# Read sensor value from each car, then feed through neuralnet, then output movement variables
	for i in range(len(cars)):

		# Initialize sensor, then read values (is there a way to prevent initialize each time)
		cars[i]['sensor'] = SimpleFrontSensor(car.model.topLeft, car.model.topRight,
									rnge = SENSOR_RANGE, angle = SENSOR_ANGLE, count = SENSOR_COUNT)
		cars[i]['sensor'].readSensor(track.walls)

		# Feed sensor value into neuralnet
		tempSensorValues = cars[i]['sensor'].outputValues()
		nnOutputValues = cars[i]['nn'].feedForward(tempSensorValues)

		