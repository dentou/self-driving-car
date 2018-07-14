"""
Author: npgh2009 & dentou
"""

import pygame, sys, random
from pygame.locals import *
from pygame.math import Vector2
from utils.Utils import *
from Point import *

class SimpleSensor(object):
	def __init__(self, rect, sensorrange = 100, sensorresolution = 1):
		"""
		Simple sensor that attaches to 4 side of the input rectangle
		"""
		self.rect = rect
		self.RANGE = sensorrange
		self.RESOLUTION = sensorresolution
		self.sensors = {'left':sensorrange, 'right':sensorrange, 'top':sensorrange, 'bottom':sensorrange}

	def readSensor(self, objectlist):
		"""
		Output sensors as a dictionary of four sensors indexed 'left','right','top','bottom'
		Each sensor output the distance from the side of the rectangle
		Maximum sensor range is self.RANGE
		Sensor resolution is self.RESOLUTION
		Sensor start from the side of the rectangle
		Increment by resolution until it detects a target object
		"""
		flag = False
	
		#Left sensor
		ssleft = self.rect.left #x-coordinate
		while (self.rect.left - ssleft) < self.RANGE: #do not run at sensor range
			for obj in objectlist:
				if isPointInsideRect(ssleft, self.rect.centery, obj):
					self.sensors['left'] = self.rect.left - ssleft
					flag = True
					break
			if flag:
				flag = False
				break
			ssleft -= self.RESOLUTION
					
		#Right sensor
		ssright = self.rect.right #x-coordinate
		while (ssright - self.rect.right) < self.RANGE:
			for obj in objectlist:
				if isPointInsideRect(ssright, self.rect.centery, obj):
					self.sensors['right'] = ssright - self.rect.right
					flag = True
					break
			if flag:
				flag = False
				break
			ssright += self.RESOLUTION
			
		#Top sensor
		sstop = self.rect.top #y-coordinate
		while (self.rect.top - sstop) < self.RANGE:
			for obj in objectlist:
				if isPointInsideRect(self.rect.centerx, sstop, obj):
					self.sensors['top'] = self.rect.top - sstop
					flag = True
					break
			if flag:
				flag = False
				break
			sstop -= self.RESOLUTION
			
		#Bottom sensor
		ssbot = self.rect.bottom #y-coordinate
		while (ssbot - self.rect.bottom) < SENSORRANGE:
			for obj in objectlist:
				if isPointInsideRect(self.rect.centerx, ssbot, obj):
					self.sensors['bottom'] = ssbot - self.rect.bottom
					flag = True
					break
			if flag:
				flag = False
				break
			ssbot += self.RESOLUTION
			
		return self.sensors

class SimpleFrontSensor(object):
	def __init__(self, PointA, PointB, rnge = 100, resolution = 1, angle = 90, count = 3):
		"""
		Sensor that attach to the middle of the input front side (defined by PointA on the left and PointB on the right)
		:param angle: angle between the leftmost sensor and rightmost sensor (in degree)
		:param count: number of sensors
		"""
		self.PointA = PointA
		self.PointB = PointB
		self.MiddleFront = Point((PointA.x + PointB.x)/2, (PointA.y + PointB.y)/2)
		self.RANGE = rnge
		self.RESOLUTION = resolution
		self.angle = angle
		self.count = count
		ss = {'dir': Vector2(1,1), 'dist': rnge}
		self.sensorList = []
		for _ in range(count):
			self.sensorList.append(dict(ss))

		self.frontSideVector = Vector2(PointA.x - PointB.x, PointA.y - PointB.y)
		angle_increment = self.angle / (self.count - 1)
		angle_offset = (180 - self.angle) / 2
		self.sensorList[0]['dir'] = rotateVector(self.frontSideVector, -angle_offset).normalize() #leftmost sensor
		self.sensorList[-1]['dir'] = rotateVector(self.frontSideVector, -(angle_offset + angle)).normalize() #rightmost sensor
		for i in range(1, count-1):
			self.sensorList[i]['dir'] = rotateVector(self.frontSideVector, - (angle_offset + angle_increment * i)).normalize() #middle sensor
		for i in range(count):
			self.sensorList[i]['pos'] = self.MiddleFront.shiftByVector(self.sensorList[i]['dir']*rnge)

	def readSensor(self, objectlist):
		"""
		Sensor start from self.MiddleFront
		Increment by self.RESOLUTION until it detects a target object
		objectlist is a list of "rectangle" to be checked for collision
		"""
		flag = False

		for i in range(self.count):
			self.sensorList[i]['pos'] = self.MiddleFront
			self.sensorList[i]['dist'] = 0
			while self.sensorList[i]['dist'] < self.RANGE:
				for obj in objectlist:
					if isPointInsideRect(self.sensorList[i]['pos'], obj):
						self.sensorList[i]['dist'] = self.sensorList[i]['dist']
						flag = True
						break
				if flag:
					flag = False
					break

				self.sensorList[i]['dist'] += self.RESOLUTION
				self.sensorList[i]['pos'] = self.sensorList[i]['pos'].shiftByVector(self.sensorList[i]['dir'] * self.RESOLUTION)