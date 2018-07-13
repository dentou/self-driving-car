"""
Random acceleration generator
Author: npgh2009
"""

import random

class AccelerationGenerator(object):
	def __init__(self, start = 0):
		self.start = start
		self.value = start

	def uniformRandom(self, start = 0, end = 100):
		self.value = random.randint(start, end) #start <= random <= end

	def periodic(self, end = 100, incre = 1):
		self.value += incre
		if self.value > end:
			self.value = self.start

class TurnspeedGenerator(object):
	def __init__(self, start = 0):
		self.start = start
		self.value = 30
		self.seed = 0

	def uniformRandom(self, start = -30, end = 30):
		self.value = random.randint(start, end) #start <= random <= end

	def zigzag(self, duration = 30, speed = 30):
		self.seed += 1
		if self.seed > duration:
			self.value = -self.value
			self.seed = 0

	def periodic(self, end = 30, incre = 1):
		self.value += incre
		if self.value > end:
			self.value = self.start
