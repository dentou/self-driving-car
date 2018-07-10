"""
Car model
Author: dentou
"""

import pygame
from pygame.math import Vector2
from model.Point import Point
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


