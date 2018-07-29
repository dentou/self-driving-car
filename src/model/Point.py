"""
Author: dentou
Adapted from https://gist.github.com/hirokai/9202782
"""

from math import sqrt, sin, cos, pi
from pygame.math import Vector2

class Point:
	def __init__(self, x_init, y_init):
		self.x = x_init
		self.y = y_init


	def asTuple(self):
		return (self.x, self.y)

	def shift(self, dx, dy):
		self.x += dx
		self.y += dy


	def shiftByVector(self, vector):
		self.x += vector.x
		self.y += vector.y


	def rotate(self, pivot, angle):
		"""
		:param pivot: pivot point
		:param angle: positive means CLOCKWISE rotation
		"""
		# positive angle means counter-clockwise rotation
		# vx = self.x - pivot.x
		# vy = self.y - pivot.y
		#
		# s = sin(angle * pi / 180)
		# c = cos(angle * pi / 180)
		#
		# new_vy = vy * c - vx * s
		# new_vx = vy * s + vx * c
		#
		# self.x = new_vx + pivot.x
		# self.y = new_vy + pivot.y

		vx = self.x - pivot.x
		vy = self.y - pivot.y

		s = sin(angle * pi / 180)
		c = cos(angle * pi / 180)

		new_vx = vx * c - vy * s
		new_vy = vx * s + vy * c

		self.x = new_vx + pivot.x
		self.y = new_vy + pivot.y

	def distanceTo(self, PointB):
		return sqrt((self.x - PointB.x) ** 2 + (self.y - PointB.y) ** 2)

	def __repr__(self):
		return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

	def __eq__(self, other):
		if self.x != other.x or self.y != other.y:
			return False
		return True


def distanceBetween(PointA, PointB):
	return sqrt((PointA.x - PointB.x) ** 2 + (PointA.y - PointB.y) ** 2)