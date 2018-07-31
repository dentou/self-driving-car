"""
Utilities
Author: dentou
"""

from Point import Point
from shapely import geometry, affinity
import pygame
from pygame.math import Vector2
from math import sin, cos, pi, atan2

def angleBetween(vectorA, vectorB):
	"""
	Return angle from vector A to vector B (positive angles for clockwise direction)
	:param vectorA:
	:param vectorB:
	:return: angle from -180 to 180
	"""
	# dot = vectorA.x * vectorB.x + vectorA.y * vectorB.y  # dot product between [xA, yA] and [xB, yB]
	# det = vectorA.x * vectorB.y - vectorA.y * vectorB.x  # determinant
	# angle = atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
	angle = vectorA.angle_to(vectorB)
	if angle < -180:
		angle += 360
	if angle > 180:
		angle -= 360
	return angle


def shiftPoint(point, dx, dy): #does not modify original point
	newPoint = affinity.translate(point.point, dx, dy)
	return Point(newPoint.x, newPoint.y)


def shiftPointByVector(point, vector): #does not modify original point
	return shiftPoint(point, vector.x, vector.y)


def rotatePoint(point, pivot, angle):
	"""
	Return rotated point around pivot (the old point is not rotated)
	:param point: point to be rotated (won't be changed)
	:param pivot: pivot point
	:param angle: in degrees, positive means counter-clockwise rotation
	:return: rotated point
	"""
	newPoint = affinity.rotate(point.point, angle, pivot.point, False)
	return Point(newPoint.x, newPoint.y)


def rotateVector(vector, angle):
	"""
	:param vector: Vector2 to be rotated (won't be changed)
	:param angle: in degrees, positive means CLOCKWISE rotation
	:return: rotated Vector2 (pygame class)
	"""
	# vx = vector.x
	# vy = vector.y
	#
	# s = sin(angle * pi / 180) # Formula for left handed coordinate system in pygame
	# c = cos(angle * pi / 180)
	#
	# new_vy = vy * c - vx * s
	# new_vx = vy * s + vx * c
	#
	# return Vector2(new_vx, new_vy)
	return vector.rotate(angle)


def lengthenVector(vector, length):
	"""
	:param vector: vector to be lengthened (won't be changed)
	:param length: length to be added
	:return: lengthened vector
	"""
	vx = vector.x
	vy = vector.y

	alpha = atan2(vy, vx)

	new_vx = vx + length * cos(alpha)
	new_vy = vy + length * sin(alpha)

	return Vector2(new_vx, new_vy)


def isPointInsideRect(PointA, rect):
	"""
	Detect if point is inside Rect
	"""
	if (PointA.point.x > rect.left) and (PointA.point.x < rect.right) and (PointA.point.y > rect.top) and (PointA.point.y < rect.bottom):
		return True
	else:
		return False

def isPointInsidePolygon(point, vertices):
	p = geometry.Point(point.asTuple())
	polygon = geometry.Polygon([vertex.asTuple() for vertex in vertices])
	return polygon.contains(p)
