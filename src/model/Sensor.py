"""
Author: npgh2009
"""

import pygame, sys, random
from pygame.locals import *
from utils.Utils import isPointInsideRect

class SimpleSensor(object):
	def __init__(self, rect, sensorrange = 100, sensorresolution = 1):
		"""
		Simple sensor that attaches to 4 side of the input rectangle
		"""
		self.rect = rect
		self.objectlist = objectlist
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
