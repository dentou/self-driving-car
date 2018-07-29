from pygame.locals import *

from Point import Point


class Camera(object):
	# todo
	def __init__(self, x, y, width, height, xMax, yMax):
		self.center = Point(x, y)
		self.width = width
		self.height = height
		self.xMax = xMax
		self.yMax = yMax

	def focus(self, targetPoint, pointList):
		dx = self.center.x - targetPoint.x
		dy = self.center.y - targetPoint.y
		for point in pointList:
			point.shift(dx, dy)



