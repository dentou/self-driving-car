"""
Author: dentou
Adapted from https://gist.github.com/hirokai/9202782
"""

from math import sqrt
from pygame.math import Vector2


class Point:
	def __init__(self, x_init, y_init):
		self.x = x_init
		self.y = y_init

	def asTuple(self):
		return (self.x, self.y)

	def shift(self, x, y):
		self.x += x
		self.y += y

	def shiftByVector(self, vector): #does not change original point
		new_x = self.x + vector.x
		new_y = self.y + vector.y
		return Point(new_x, new_y)

	def distanceTo(self, PointB):
		return sqrt((self.x - PointB.x) ** 2 + (self.y - PointB.y) ** 2)

	def __repr__(self):
		return "".join(["Point(", str(self.x), ",", str(self.y), ")"])


def distanceBetween(PointA, PointB):
	return sqrt((PointA.x - PointB.x) ** 2 + (PointA.y - PointB.y) ** 2)