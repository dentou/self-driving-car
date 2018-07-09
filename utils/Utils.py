import pygame
import sys
import math
from math import sqrt, cos, sin


def draw_line_with_circles(screen, color, start, end, thickness):
	"""
	Draw line by combining adjacent circles
	:param screen:
	:param color:
	:param start:
	:param end:
	:param thickness:
	:return:
	"""
	dx = start[0] - end[0]
	dy = start[1] - end[1]
	iterations = max(abs(dx), abs(dy))

	for i in range(iterations):
		progress = 1.0 * i / iterations
		aprogress = 1 - progress
		x = int(aprogress * start[0] + progress * end[0])
		y = int(aprogress * start[1] + progress * end[1])
		pygame.draw.circle(screen, color, (x, y), thickness)




def draw_segment(screen, color, start, end, width=100, centerThickness=3, borderThickness=10):
	"""
	Draw track segment
	:param screen:
	:param color:
	:param start:
	:param end:
	:param width:
	:param centerThickness:
	:param borderThickness:
	:return:
	"""
	vector = (end[0] - start[0], end[1] - start[1])
	norm = sqrt(vector[0] ** 2 + vector[1] ** 2)
	perpVector = (-1 * vector[1] / norm, vector[0] / norm)

	# Draw center line
	pygame.draw.lines(screen, color, False, [start, end], centerThickness)
	#draw_line_with_circles(screen, color, start, end, centerThickness)

	# Draw "left" border line
	leftStart = (round(start[0] + perpVector[0] * width / 2), round(start[1] + perpVector[1] * width / 2))
	leftEnd = (round(end[0] + perpVector[0] * width / 2), round(end[1] + perpVector[1] * width / 2))
	#pygame.draw.lines(screen, color, False, [leftStart, leftEnd], borderThickness)
	draw_line_with_circles(screen, color, leftStart, leftEnd, borderThickness)


	# Draw "right" border line
	rightStart = (round(start[0] - perpVector[0] * width / 2), round(start[1] - perpVector[1] * width / 2))
	rightEnd = (round(end[0] - perpVector[0] * width / 2), round(end[1] - perpVector[1] * width / 2))
	#pygame.draw.lines(screen, color, False, [rightStart, rightEnd], borderThickness)
	draw_line_with_circles(screen, color, rightStart, rightEnd, borderThickness)



def draw_track(screen, color, pointList):
	"""
	Draw track
	:param screen:
	:param color:
	:param pointList:
	:return:
	"""
	for index, point in enumerate(pointList[:-1]):
		draw_segment(screen, color, point, pointList[index + 1])



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

	pointList = []
	for angle in range(360):
		x = 300 + 100*cos(angle * math.pi / 180)
		y = 300 + 100*sin(angle * math.pi / 180)
		pointList.append((x, y))

	draw_track(screen, BLACK, pointList)

	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
