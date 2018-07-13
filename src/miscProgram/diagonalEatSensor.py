"""
Author: npgh2009
Some code from inventwithpython
"""

import pygame, sys, random
from pygame.locals import *

def doRectsOverlap(rect1, rect2):
	"""
	Detect if the two rectangle overlap
	"""
	for a, b in [(rect1, rect2), (rect2, rect1)]:
		if isPointInsideRect(a.left, a.top, b):
			print('({},{})'.format(a.left, a.top)) #print position of collision
			return True
		elif isPointInsideRect(a.left, a.bottom, b):
			print('({},{})'.format(a.left, a.bottom))
			return True
		elif isPointInsideRect(a.right, a.top, b):
			print('({},{})'.format(a.right, a.top))
			return True
		elif isPointInsideRect(a.right, a.bottom, b):
			print('({},{})'.format(a.right, a.bottom))
			return True

	return False

def isPointInsideRect(x, y, rect):
	"""
	Detect if point is inside Rect
	"""
	if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
		return True
	else:
		return False
		
# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Eating sensor')

# set up direction variables
DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9
DOWN = 2
UP = 8
LEFT = 4
RIGHT = 6

MOVESPEED = 4

# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# set up the bouncer and food data structures
foodCounter = 0
# eatCounter = 0
NEWFOOD = 20
FOODSIZE = 15
SENSORRANGE = 100
SENSORRESOLUTION = 20 #incremental step of sensor reading
SENSORSIZE = 3
bouncer = {'rect':pygame.Rect(300, 100, 50, 50), 'dir':UPRIGHT}
foods = []
for i in range(20):
	foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), \
			random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

			
def readSensor(rect, foods):
	"""
	Output sensors as a dictionary of four sensors indexed 'left','right','top','bottom'
	Each sensor output the distance from the side of the rect
	Maximum sensor range is SENSORRANGE
	Sensor resolution is SENSORRESOLUTION
	Sensor start from the side of the bouncer
	Increment by resolution until it detects a piece of food
	Cannot detect wall (simply return SENSORRANGE)
	"""
	sensors = {'left':SENSORRANGE, 'right':SENSORRANGE, 'top':SENSORRANGE, 'bottom':SENSORRANGE}
	flag = False
	
	#Left sensor
	ssleft = rect.left #x-coordinate
	while (rect.left - ssleft) < SENSORRANGE: #do not run at range SENSORRANGE
		for food in foods:
			if isPointInsideRect(ssleft, rect.centery, food):
				sensors['left'] = rect.left - ssleft
				flag = True
				break
		if flag:
			flag = False
			break
		ssleft -= SENSORRESOLUTION
				
	#Right sensor
	ssright = rect.right #x-coordinate
	while (ssright - rect.right) < SENSORRANGE:
		for food in foods:
			if isPointInsideRect(ssright, rect.centery, food):
				sensors['right'] = ssright - rect.right
				break
		if flag:
			flag = False
			break
		ssright += SENSORRESOLUTION
		
	#Top sensor
	sstop = rect.top #y-coordinate
	while (rect.top - sstop) < SENSORRANGE:
		for food in foods:
			if isPointInsideRect(rect.centerx, sstop, food):
				sensors['top'] = rect.top - sstop
				break
		if flag:
			flag = False
			break
		sstop -= SENSORRESOLUTION
		
	#Bottom sensor
	ssbot = rect.bottom #y-coordinate
	while (ssbot - rect.bottom) < SENSORRANGE:
		for food in foods:
			if isPointInsideRect(rect.centerx, ssbot, food):
				sensors['bottom'] = ssbot - rect.bottom
				break
		if flag:
			flag = False
			break
		ssbot += SENSORRESOLUTION
		
	return sensors
			
# run the game loop
while True:
	# check for the QUIT event
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	foodCounter += 1
	if foodCounter >= NEWFOOD:
		# add new food
		foodCounter = 0
		foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

	# draw the black background onto the surface
	windowSurface.fill(BLACK)
	
	# change direction when no food is eaten after a period of time
	# if eatCounter >= 500:
		# bouncer['dir'] = random.choice([DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT])
		# eatCounter = 0

	# move the bouncer data structure
	if bouncer['dir'] == DOWNLEFT:
		bouncer['rect'].left -= MOVESPEED
		bouncer['rect'].top += MOVESPEED
	if bouncer['dir'] == DOWNRIGHT:
		bouncer['rect'].left += MOVESPEED
		bouncer['rect'].top += MOVESPEED
	if bouncer['dir'] == UPLEFT:
		bouncer['rect'].left -= MOVESPEED
		bouncer['rect'].top -= MOVESPEED
	if bouncer['dir'] == UPRIGHT:
		bouncer['rect'].left += MOVESPEED
		bouncer['rect'].top -= MOVESPEED
	if bouncer['dir'] == DOWN:
		bouncer['rect'].top += MOVESPEED
	if bouncer['dir'] == UP:
		bouncer['rect'].top -= MOVESPEED

	# check if the bouncer has move out of the window
	if bouncer['rect'].top < 0:
		# bouncer has moved past the top
		if bouncer['dir'] == UPLEFT:
			bouncer['dir'] = DOWNLEFT
		if bouncer['dir'] == UPRIGHT:
			bouncer['dir'] = DOWNRIGHT
		if bouncer['dir'] == UP:
			bouncer['dir'] = DOWN
	if bouncer['rect'].bottom > WINDOWHEIGHT:
		# bouncer has moved past the bottom
		if bouncer['dir'] == DOWNLEFT:
			bouncer['dir'] = UPLEFT
		if bouncer['dir'] == DOWNRIGHT:
			bouncer['dir'] = UPRIGHT
		if bouncer['dir'] == DOWN:
			bouncer['dir'] = UP
	if bouncer['rect'].left < 0:
		# bouncer has moved past the left side
		if bouncer['dir'] == DOWNLEFT:
			bouncer['dir'] = DOWNRIGHT
		if bouncer['dir'] == UPLEFT:
			bouncer['dir'] = UPRIGHT
	if bouncer['rect'].right > WINDOWWIDTH:
		# bouncer has moved past the right side
		if bouncer['dir'] == DOWNRIGHT:
			bouncer['dir'] = DOWNLEFT
		if bouncer['dir'] == UPRIGHT:
			bouncer['dir'] = UPLEFT
			
	

	# draw the bouncer onto the surface
	pygame.draw.rect(windowSurface, WHITE, bouncer['rect'])

	# check if the bouncer has intersected with any food squares.
	for food in foods[:]:
		if doRectsOverlap(bouncer['rect'], food):
			print('Collision detected')
			foods.remove(food)
	
	#read sensors
	sensors = readSensor(bouncer['rect'], foods)
	
	#change dir base on closest sensors, if no sensors work then keep dir
	#need improvement
	if (sensors['left'] < sensors['right']):
		if (sensors['top'] < sensors['bottom']):
			bouncer['dir'] = UPLEFT
		elif (sensors['bottom'] < sensors['top']):
			bouncer['dir'] = DOWNLEFT
		elif bouncer['dir'] == UPRIGHT:
			bouncer['dir'] = UPLEFT
		elif bouncer['dir'] == DOWNRIGHT:
			bouncer['dir'] = DOWNLEFT
	elif (sensors['right'] < sensors['left']):
		if (sensors['top'] < sensors['bottom']):
			bouncer['dir'] = UPRIGHT
		elif (sensors['bottom'] < sensors['top']):
			bouncer['dir'] = DOWNRIGHT
		elif bouncer['dir'] == UPLEFT:
			bouncer['dir'] = UPRIGHT
		elif bouncer['dir'] == DOWNLEFT:
			bouncer['dir'] = DOWNRIGHT
	elif (sensors['top'] < sensors['bottom']):
		if (sensors['left'] < sensors['right']):
			bouncer['dir'] = UPLEFT
		elif (sensors['right'] < sensors['left']):
			bouncer['dir'] = UPRIGHT
		elif bouncer['dir'] == DOWNLEFT:
			bouncer['dir'] = UPLEFT
		elif bouncer['dir'] == DOWNRIGHT:
			bouncer['dir'] = UPRIGHT
	elif (sensors['bottom'] < sensors['top']):
		if (sensors['left'] < sensors['right']):
			bouncer['dir'] = DOWNLEFT
		elif (sensors['right'] < sensors['left']):
			bouncer['dir'] = DOWNRIGHT
		elif bouncer['dir'] == UPLEFT:
			bouncer['dir'] = DOWNLEFT
		elif bouncer['dir'] == UPRIGHT:
			bouncer['dir'] = DOWNRIGHT
	
	# draw the food
	for i in range(len(foods)):
		pygame.draw.rect(windowSurface, GREEN, foods[i])
		
	# draw the sensor
	if sensors['left'] < SENSORRANGE:
		pygame.draw.circle(windowSurface, RED, (bouncer['rect'].left-sensors['left'],
					bouncer['rect'].centery), SENSORSIZE, 0)
	if sensors['right'] < SENSORRANGE:
		pygame.draw.circle(windowSurface, RED, (bouncer['rect'].right+sensors['right'],
					bouncer['rect'].centery), SENSORSIZE, 0)
	if sensors['top'] < SENSORRANGE:
		pygame.draw.circle(windowSurface, RED, (bouncer['rect'].centerx,
					bouncer['rect'].top-sensors['top']), SENSORSIZE, 0)
	if sensors['bottom'] < SENSORRANGE:
		pygame.draw.circle(windowSurface, RED, (bouncer['rect'].centerx,
					bouncer['rect'].bottom+sensors['bottom']), SENSORSIZE, 0)

	# draw the window onto the screen
	pygame.display.update()
	mainClock.tick(30)
