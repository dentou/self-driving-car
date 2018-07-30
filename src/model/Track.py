"""
Track model
Author: dentou
"""


import pygame
import sys
from math import *
from math import sqrt, cos, sin, radians
from utils.Utils import *

class Track:

	DEFAULT_WIDTH = 100

	def __init__(self, centerPoints, widthMap, screen, color, centerLineThickness, borderLineThickness):
		"""

		:param centerPoints: List Point objects
		:param widthMap: Dictionary (map) of {point:width} items, where width is the width of track at this point to next one
		:param screen:
		:param color:
		:param centerLineThickness:
		:param borderLineThickness:
		"""
		self.centerPoints = centerPoints
		self.widthMap = widthMap
		self.screen = screen
		self.color = color
		self.centerLineThickness = centerLineThickness
		self.borderLineThickness = borderLineThickness


	def generateBorderPoints(self):
		self.leftBorderPoints = []
		self.rightBorderPoints = []
		self.__generateStartBorderPoints()
		self.__generateMiddleBorderPoints()
		self.__generateEndBorderPoints()


	def __generateMiddleBorderPoints(self):
		for i in range(1, len(self.centerPoints) - 1):
			previous = self.centerPoints[i-1]
			now = self.centerPoints[i]
			next = self.centerPoints[i+1]

			vp = Vector2(previous.x - now.x, previous.y - now.y).normalize()
			vn = Vector2(next.x - now.x, next.y - now.y).normalize()

			angle = angleBetween(vp, vn)
			# print("Angle: ", angle)

			w1 = self.widthMap[previous] / 2
			w2 = self.widthMap[now] / 2

			x = (w1 + w2 * cos(radians(angle))) / sin(radians(angle))
			# print("x = ", x)
			normalVector = rotateVector(vn, -90)

			self.leftBorderPoints.append(shiftPointByVector(now, normalVector * w2 + vn * x))
			self.rightBorderPoints.append(shiftPointByVector(now, -normalVector * w2 - vn * x))


	def __generateStartBorderPoints(self):
		startPoint = self.centerPoints[0]
		nextPoint = self.centerPoints[1]

		width = self.widthMap[startPoint]

		dirVector = Vector2(nextPoint.x - startPoint.x, nextPoint.y - startPoint.y)
		normalVector = rotateVector(dirVector, -90).normalize()

		self.leftBorderPoints.append(shiftPointByVector(startPoint, normalVector * width / 2))
		self.rightBorderPoints.append(shiftPointByVector(startPoint, rotateVector(normalVector, 180) * width / 2))


	def __generateEndBorderPoints(self):
		endPoint = self.centerPoints[-1]
		previousPoint = self.centerPoints[-2]

		width = self.widthMap[previousPoint]

		dirVector = Vector2(endPoint.x - previousPoint.x, endPoint.y - previousPoint.y)
		normalVector = rotateVector(dirVector, -90).normalize()

		self.leftBorderPoints.append(shiftPointByVector(endPoint, normalVector * width / 2))
		self.rightBorderPoints.append(shiftPointByVector(endPoint, rotateVector(normalVector, 180) * width / 2))


	def draw(self):
		pygame.draw.lines(self.screen, self.color, False,[point.asFuncTuple(ceil) for point in self.centerPoints], self.centerLineThickness)
		pygame.draw.lines(self.screen, self.color, False, [point.asFuncTuple(ceil) for point in (self.leftBorderPoints + list(reversed(self.rightBorderPoints)))], self.borderLineThickness)


	def collidedWithPolygon(self, pointList):
		""""
		Return track checkpoint where one of the points in pointList collided with
		"""
		for point in pointList:
			checkpoint = self.collidedWithPoint(point)
			if checkpoint > 0:
				return checkpoint
		return -1

	def collidedWithPoint(self, point):
		""""
		Return track checkpoint where point collided with
		Example: 2.6 means point collided with track between checkpoint 2 and 3 and at 60% distance from checkpoint 2 to 3
		"""
		minDist = point.distanceToLine(self.centerPoints[0], self.centerPoints[1])
		index = 0
		for i in range(1, len(self.centerPoints) - 1):
			dist = point.distanceToLine(self.centerPoints[i], self.centerPoints[i+1])
			if dist < minDist:
				index = i
				minDist = dist
		if 2 * minDist >= self.widthMap[self.centerPoints[index]]: # collided
			tangentVector = self.centerPoints[index].vectorTo(self.centerPoints[index + 1])
			posVector = self.centerPoints[index].vectorTo(point)
			segmentTravelled = tangentVector.dot(posVector)/(tangentVector.length() * cos(radians(angleBetween(tangentVector, posVector))))
			checkpoint =  index + segmentTravelled / tangentVector.length()
			return checkpoint
		return -1


if __name__ == "__main__":
	# Set up the colors.
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)

	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	screen.fill(WHITE)
	clock = pygame.time.Clock()

	pointList = [Point(100, 100), Point(400, 100), Point(200, 400), Point(500, 500)]
	widthMap = dict()
	widthMap[pointList[0]] = 100
	widthMap[pointList[1]] = 75
	widthMap[pointList[2]] = 120
	# pointList = []
	# for angle in range(361):
	# 	x = 300 + 100*cos(radians(angle))
	# 	y = 300 + 100*sin(radians(angle))
	# 	pointList.append(Point(x, y))


	track = Track(pointList, widthMap, screen, BLACK, 2, 7)
	track.generateBorderPoints()
	print(track.centerPoints)
	print(track.leftBorderPoints)
	print(track.rightBorderPoints)
	track.draw()
	# drawTrack(screen, BLACK, pointList)

	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
