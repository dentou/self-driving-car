"""
Author: dentou
Adapted from https://gist.github.com/hirokai/9202782
"""

from math import sqrt


class Point:
	def __init__(self, x_init, y_init):
		self.x = x_init
		self.y = y_init

	def asTuple(self):
		return self.x, self.y

	def shift(self, x, y):
		self.x += x
		self.y += y

	def __repr__(self):
		return "".join(["Point(", str(self.x), ",", str(self.y), ")"])


def distance(a, b):
	return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
