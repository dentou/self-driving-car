"""
Author: dentou
Adapted from https://gist.github.com/hirokai/9202782
"""

from math import sqrt, sin, cos, pi
from pygame.math import Vector2
from shapely import geometry, affinity

import numpy as np


class Point:
	def __init__(self, x_init, y_init):
		self.point = geometry.Point(x_init, y_init)


	def __repr__(self):
		return "".join(["Point(", str(self.point.x), ",", str(self.point.y), ")"])

	def __eq__(self, other):
		return self.point.equals(other.point)

	def __ne__(self, other):
		return not(self == other)

	def __hash__(self):
		return hash((self.point.x, self.point.y))

	def asFuncTuple(self, func):
		return (func(self.point.x), func(self.point.y))


	def asTuple(self):
		return self.point.coords[0]

	def asShapelyPoint(self):
		return self.point

	def vectorTo(self, other):
		return Vector2(other.point.x - self.point.x, other.point.y - self.point.y)

	def shift(self, dx, dy):
		self.point = affinity.translate(self.point, dx, dy)


	def shiftByVector(self, vector):
		self.shift(vector.x, vector.y)


	def rotate(self, pivot, angle):
		"""
		:param pivot: pivot point
		:param angle: positive means CLOCKWISE rotation
		"""

		# vx = self.x - pivot.x
		# vy = self.y - pivot.y
		#
		# s = sin(angle * pi / 180)
		# c = cos(angle * pi / 180)
		#
		# new_vx = vx * c - vy * s
		# new_vy = vx * s + vy * c
		#
		# self.x = new_vx + pivot.x
		# self.y = new_vy + pivot.y
		self.point = affinity.rotate(self.point, angle, pivot.point, False)

	def distanceTo(self, other):
		return self.point.distance(other.point)

	def distanceToLine(self, pointA, pointB):
		# p = np.asarray(self.asTuple())
		# pA = np.asarray(pointA.asTuple())
		# pB = np.asarray(pointB.asTuple())
		# d = np.linalg.norm(np.cross(pB - pA, pA - p)) / np.linalg.norm(pB - pA)
		line = geometry.LineString(pointA.point, pointB.point)
		d = self.point.distance(line)
		return d


def distanceBetween(PointA, PointB):
	return PointA.distanceTo(PointB)