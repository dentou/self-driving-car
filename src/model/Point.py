"""
Author: dentou
Adapted from https://gist.github.com/hirokai/9202782
"""

from math import sqrt, sin, cos, pi
from pygame.math import Vector2
import numpy as np


class Point:
	def __init__(self, x_init, y_init):
		self.x = x_init
		self.y = y_init

	def __repr__(self):
		return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

	def __eq__(self, other):
		return (self.x, self.y) == (other.x, other.y)

	def __ne__(self, other):
		return not(self == other)

	def __hash__(self):
		return hash((self.x, self.y))

	def asFuncTuple(self, func):
		return (func(self.x), func(self.y))


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

	def distanceToLine(self, pointA, pointB):
		# num = abs((pointB.y - pointA.y) * self.x - (pointB.x - pointA.x) * self.y + pointB.x * pointA.y - pointB.y * pointA.x)
		# den = sqrt((pointB.x - pointA.x) ** 2 + (pointB.y - pointA.y) ** 2)
		# return num/den
		p = np.asarray(self.asTuple())
		pA = np.asarray(pointA.asTuple())
		pB = np.asarray(pointB.asTuple())
		d = np.linalg.norm(np.cross(pB - pA, pA - p)) / np.linalg.norm(pB - pA)
		return d


def distanceBetween(PointA, PointB):
	return sqrt((PointA.x - PointB.x) ** 2 + (PointA.y - PointB.y) ** 2)