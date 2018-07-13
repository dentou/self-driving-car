"""
Car model
Author: dentou
"""

import pygame, sys
from pygame.math import Vector2
from Point import Point
from utils.Utils import *


class Car:

	def __init__(self, position=(0, 0), size=(50, 100), speed=0, acceleration=0):
		self.direction = Vector2(0, -1).normalize()
		self.speed = speed
		self.acceleration = acceleration
		self.model = Model(position[0], position[1], size[0], size[1])
		self.is_braking = False

	def draw(self, surface, color):
		pygame.draw.polygon(surface, color, self.model.get_point_list())

	def reset(self, position=(0, 0), size=(50, 100), speed=0, acceleration=0):
		self.model = Model(position[0], position[1], size[0], size[1])
		self.speed = speed
		self.acceleration = acceleration
		self.direction = Vector2(0, -1).normalize()

	def accelerate(self, value):
		"""
		Set acceleration of the car
		:param value: acceleration
		"""
		self.is_braking = False
		self.acceleration = value

	def brake(self, value=100):
		"""
		Brake the car by applying counter acceleration
		:param value: magnitude of acceleration
		"""
		self.is_braking = True
		if self.speed > 0:
			self.acceleration = -value
		else:
			self.acceleration = value

	def is_moving(self):
		"""
		Check if car is moving
		:return: boolean
		"""
		return self.speed != 0

	def turn(self, angle):
		"""
		Turn the car by angle
		:param angle: in degrees, positive means counter-clockwise rotation
		"""
		# Rotate direction vector
		self.direction = rotate_vector(self.direction, angle)
		# Rotate car model
		self.model.rotate(angle)

	def update(self, time_interval):
		"""
		Update car parameters
		:param time_interval: in seconds
		"""
		displacement = self.direction * (self.speed * time_interval + 0.5 * self.acceleration * time_interval ** 2)
		self.model.move(displacement.x, displacement.y)
		self.speed += self.acceleration * time_interval
		if self.is_braking:
			if self.acceleration * self.speed > 0:
				self.speed = 0
				self.acceleration = 0
				self.is_braking = False


class Model:
	"""
	Model of the car as a rectangle
	"""
	def __init__(self, left, top, width, height):
		self.top_left = Point(left, top)
		self.top_right = Point(left + width, top)
		self.bottom_left = Point(left, top + height)
		self.bottom_right = Point(left + width, top + height)

	def get_point_list(self):
		"""
		:return: list of points as tuples
		"""
		return [self.top_left.as_tuple(), self.top_right.as_tuple(), self.bottom_right.as_tuple(),
				self.bottom_left.as_tuple()]

	def move(self, dx, dy):
		"""
		Shift model
		"""
		self.top_left.shift(dx, dy)
		self.top_right.shift(dx, dy)
		self.bottom_left.shift(dx, dy)
		self.bottom_right.shift(dx, dy)

	def get_center(self):
		center_x = (self.top_left.x + self.bottom_right.x) / 2
		center_y = (self.top_left.y + self.bottom_right.y) / 2
		return center_x, center_y

	def rotate(self, angle):
		new_top_left = rotate_point(self.top_left, Point(*self.get_center()), angle)
		new_top_right = rotate_point(self.top_right, Point(*self.get_center()), angle)
		new_bottom_left = rotate_point(self.bottom_left, Point(*self.get_center()), angle)
		new_bottom_right = rotate_point(self.bottom_right, Point(*self.get_center()), angle)

		self.top_left = new_top_left
		self.top_right = new_top_right
		self.bottom_left = new_bottom_left
		self.bottom_right = new_bottom_right

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
	WINDOWWIDTH = 600
	WINDOWHEIGHT = 600
	windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
	pygame.display.set_caption('Car test')

	# Set up the colors.
	BLACK = (0, 0, 0)
	GREEN = (0, 255, 0)
	WHITE = (255, 255, 255)

	# Set speed parameters
	ACCELERATION = 100
	BRAKE = 100
	TURNSPEED = 30

	# Setup car
	x0 = 300
	y0 = 300
	CARWIDTH = 20
	CARHEIGHT = 40
	car = Car(position=(x0, y0), size=(CARWIDTH, CARHEIGHT))

	# Choose whether to set car when going out of window
	CARRESET = True

	# Set up movement variables.
	moveUp = False
	moveDown = False
	moveLeft = False
	moveRight = False

	MOVESPEED = 4

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
			car.accelerate(ACCELERATION)
		if moveDown:
			car.accelerate(-ACCELERATION)
		if car.is_moving():
			if moveLeft:
				car.turn(TURNSPEED / FPS)  # 30 degrees per second
			elif moveRight:
				car.turn(-TURNSPEED / FPS)
			if (not moveUp) and (not moveDown) and car.is_moving():
				car.brake(BRAKE)

		car.update(1 / FPS)

		# If car goes out of window, reset
		if CARRESET:
			if ((car.model.top_left.x < 0) or (car.model.top_right.x < 0) or (car.model.bottom_left.x < 0) or (
					car.model.bottom_right.x < 0) or
					(car.model.top_left.x > WINDOWWIDTH) or (car.model.top_right.x > WINDOWWIDTH) or (
							car.model.bottom_left.x > WINDOWWIDTH) or
					(car.model.bottom_right.x > WINDOWWIDTH) or
					(car.model.top_left.y < 0) or (car.model.top_right.y < 0) or (car.model.bottom_left.y < 0) or (
							car.model.bottom_right.y < 0) or
					(car.model.top_left.y > WINDOWHEIGHT) or (car.model.top_right.y > WINDOWHEIGHT) or (
							car.model.bottom_left.y > WINDOWHEIGHT) or
					(car.model.bottom_right.y > WINDOWHEIGHT)):
				car.reset(position=(x0, y0), size=(CARWIDTH, CARHEIGHT))

		# Draw the white background onto the surface.
		windowSurface.fill(WHITE)

		# Draw small circle to check if camera is moving with car (then the circle will move in reverse direction)
		pygame.draw.circle(windowSurface, BLACK, (50, 50), 20)

		# Draw car
		car.draw(windowSurface, BLACK)

		# Draw the window onto the screen.
		pygame.display.update()
		mainClock.tick(FPS)


if __name__=="__main__":
	main()

