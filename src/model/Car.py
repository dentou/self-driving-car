"""
Car model
Author: dentou & npgh2009
"""

import pygame, sys
from pygame.math import Vector2
from pygame.locals import *
from Point import Point
from utils.Utils import *
from Camera import Camera
from Track import Track


class Car:
	"""
	Parameters:
		direction: # Direction of movement (generally not the same as vector from back to front - the car may move backward)
		velocity: scalar velocity w.r.t direction
		acceleration: applied scalar acceleration w.r.t to direction
		totalAcceleration: = acceleration + drag
	"""
	DEFAULT_DIRECTION = (0, -1)
	DEFAULT_BRAKING_ACCELERATION = 100
	DRAG_COEFF = 1.33 # unit: 1/sec; settling time = 4 / DRAG_COEFF =  3 sec
	VELOCITY_THRESHOLD = 0.5 # if velocity < threshold then the car will not move
	ACCELERATION_THRESHOLD = 5

	def __init__(self, position=(0, 0), direction=DEFAULT_DIRECTION, size=(50, 100), velocity=0, acceleration=0):
		self.reset(position, direction, size, velocity, acceleration)

	def draw(self, surface, color):
		pygame.draw.polygon(surface, color, self.model.getPointList())

	def reset(self, position=(0, 0), direction=DEFAULT_DIRECTION, size=(50, 100), velocity=0, acceleration=0):
		self.direction = Vector2(self.DEFAULT_DIRECTION).normalize()
		self.velocity = velocity
		self.acceleration = acceleration
		self.totalAcceleration = acceleration
		self.model = Model(position[0], position[1], size[0], size[1])
		self.isBraking = False

		self.turn(angleBetween(Vector2(self.DEFAULT_DIRECTION), Vector2(direction)))

	def accelerate(self, value):
		"""
		Set acceleration of the car
		:param value: acceleration
		"""
		if abs(value) > self.ACCELERATION_THRESHOLD:
			self.acceleration = value
		else:
			self.acceleration = 0

	def brake(self, value=DEFAULT_BRAKING_ACCELERATION):
		"""
		Brake the car by applying counter acceleration
		:param value: magnitude of acceleration
		"""
		if not self.isMoving():
			pass

		self.isBraking = True
		if self.velocity > 0:
			self.accelerate(-value)
		elif self.velocity < 0:
			self.accelerate(value)

	def unbrake(self):
		self.isBraking = False
		self.accelerate(0)

	def isMoving(self):
		"""
		Check if car is moving
		:return: boolean
		"""
		return self.velocity != 0

	def turn(self, angle):
		"""
		Turn the car by angle
		:param angle: from -180 degrees to 180 degrees, positive means CLOCKWISE rotation
		"""
		# Rotate direction vector
		self.direction = rotateVector(self.direction, angle)
		# Rotate car model
		self.model.rotate(angle)

	def isCollideWithRect(self, rect):
		"""
		Check if car has collided with input pygame.Rect object
		"""
		if (isPointInsideRect(self.model.topLeft, rect) or isPointInsideRect(self.model.topRight, rect)
			or isPointInsideRect(self.model.bottomLeft, rect) or isPointInsideRect(self.model.bottomRight, rect)):
			return True
		return False

	def isCollidedWithTrack(self, track):
		return track.collidedWithPolygon(self.model.pointList)


	def update(self, timeInterval):
		"""
		Update car parameters
		:param timeInterval: in seconds
		"""
		# Calculate total acceleration
		dragAcceleration = -self.DRAG_COEFF * self.velocity
		self.totalAcceleration = self.acceleration + dragAcceleration

		displacement = self.direction * (self.velocity * timeInterval + 0.5 * self.totalAcceleration * timeInterval ** 2)
		self.model.move(displacement.x, displacement.y)
		self.velocity += self.totalAcceleration * timeInterval

		if self.isBraking:
			if self.totalAcceleration * self.velocity > 0:
				self.velocity = 0
				self.totalAcceleration = 0
				self.isBraking = False

		if abs(self.velocity) < self.VELOCITY_THRESHOLD:
			self.velocity = 0


class Model:
	"""
	Model of the car as a rectangle
	"""
	def __init__(self, left, top, width, height):
		self.topLeft = Point(left, top)
		self.topRight = Point(left + width, top)
		self.bottomLeft = Point(left, top + height)
		self.bottomRight = Point(left + width, top + height)
		self.pointList = [self.topLeft, self.topRight, self.bottomRight, self.bottomLeft]

	def getPointList(self):
		"""
		:return: list of points as tuples
		"""
		return [point.asTuple() for point in self.pointList]

	def move(self, dx, dy):
		"""
		Shift model
		"""
		for point in self.pointList:
			point.shift(dx, dy)

	def getCenter(self):
		center_x = (self.topLeft.x + self.bottomRight.x) / 2
		center_y = (self.topLeft.y + self.bottomRight.y) / 2
		return Point(center_x, center_y)

	def rotate(self, angle):
		center = self.getCenter().asTuple()
		for point in self.pointList:
			point.rotate(Point(*center), angle)



def main():
	"""
	Test function
	"""
	# set up pygame
	pygame.init()
	mainClock = pygame.time.Clock()

	# Set game parameters
	FPS = 60

	# set up the window
	WINDOW_WIDTH = 600
	WINDOW_HEIGHT = 600
	windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
	pygame.display.set_caption('Car test')

	# Setup world's parameter
	WORLD_WIDTH = 1200
	WORLD_HEIGHT = 1200
	pointList = []
	camera = Camera(300, 300, 100, 100, WORLD_WIDTH, WINDOW_HEIGHT)

	# Set up the colors.
	BLACK = (0, 0, 0)
	GREEN = (0, 255, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)

	# Set speed parameters
	ACCELERATION = 100 # pixels per second squared
					# final speed will be ACCELERATION / DRAG_COEFF
	BRAKING_ACCELERATION = 300
	TURN_SPEED = 45 # degrees per second

	# Setup circle for camera scrolling detection
	circleCenter = Point(50, 50)
	pointList.append(circleCenter)

	# Setup car
	x0 = 300
	y0 = 300
	CAR_WIDTH = 20
	CAR_HEIGHT = 40
	car = Car(position=(x0, y0), direction=(1,0), size=(CAR_WIDTH, CAR_HEIGHT))
	# Add car points to point list
	pointList.extend(car.model.pointList)

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
					#car.brake(BRAKING_ACCELERATION)
					car.accelerate(0)
					pass

		car.update(1 / FPS)

		#camera.focus(car.model.getCenter(), pointList)

		# If car goes out of window, reset
		# if CAR_RESET:
		# 	if ((car.model.topLeft.x < 0) or (car.model.topRight.x < 0) or (car.model.bottomLeft.x < 0) or (
		# 			car.model.bottomRight.x < 0) or
		# 			(car.model.topLeft.x > WINDOW_WIDTH) or (car.model.topRight.x > WINDOW_WIDTH) or (
		# 					car.model.bottomLeft.x > WINDOW_WIDTH) or
		# 			(car.model.bottomRight.x > WINDOW_WIDTH) or
		# 			(car.model.topLeft.y < 0) or (car.model.topRight.y < 0) or (car.model.bottomLeft.y < 0) or (
		# 					car.model.bottomRight.y < 0) or
		# 			(car.model.topLeft.y > WINDOW_HEIGHT) or (car.model.topRight.y > WINDOW_HEIGHT) or (
		# 					car.model.bottomLeft.y > WINDOW_HEIGHT) or
		# 			(car.model.bottomRight.y > WINDOW_HEIGHT)):
		# 		car.reset(position=(x0, y0), size=(CAR_WIDTH, CAR_HEIGHT))


		# Draw the white background onto the surface.
		windowSurface.fill(WHITE)

		# Draw small circle to check if camera is moving with car (then the circle will move in reverse direction)
		circleCenter.x = int(circleCenter.x)
		circleCenter.y = int(circleCenter.y)
		pygame.draw.circle(windowSurface, BLACK, circleCenter.asTuple(), 20)

		# Draw car
		car.draw(windowSurface, BLACK)

		# Set up fonts.
		basicFont = pygame.font.SysFont(None, 24)

		# Setup information text
		TEXT_X0 = WINDOW_WIDTH - 275
		TEXT_Y0 = 10
		TEXT_VGAP = 15
		# Position
		posText = basicFont.render(
			"(x,y) = ({0:.0f},{1:.0f})".format(car.model.getCenter().x, car.model.getCenter().y), True, BLACK)
		posRect = posText.get_rect()
		posRect.topleft = (TEXT_X0, TEXT_Y0)
		# Velocity
		velText = basicFont.render("velocity = {0:.0f} pixels/s".format(car.velocity), True, BLACK)
		velRect = velText.get_rect()
		velRect.topleft = (TEXT_X0, TEXT_Y0 + TEXT_VGAP)
		# Acceleration
		accText = basicFont.render("acceleration = {0:.0f} pixels/s^2".format(car.acceleration), True, BLACK)
		accRect = accText.get_rect()
		accRect.topleft = (TEXT_X0, TEXT_Y0 + 2 * TEXT_VGAP)
		# Total Acceleration
		totAccText = basicFont.render("total acceleration = {0:.0f} pixels/s^2".format(car.totalAcceleration), True, BLACK)
		totAccRect = totAccText.get_rect()
		totAccRect.topleft = (TEXT_X0, TEXT_Y0 + 3 * TEXT_VGAP)
		# Stop notification
		if not car.isMoving():
			stopText = basicFont.render("Stopped", True, RED)
			stopRect = stopText.get_rect()
			stopRect.topleft = (TEXT_X0, TEXT_Y0 + 4 * TEXT_VGAP)
			windowSurface.blit(stopText, stopRect)

		# Display car parameters
		windowSurface.blit(posText, posRect)
		windowSurface.blit(velText, velRect)
		windowSurface.blit(accText, accRect)
		windowSurface.blit(totAccText, totAccRect)


		# Draw the window onto the screen.
		pygame.display.update()
		mainClock.tick(FPS)


if __name__=="__main__":
	main()

