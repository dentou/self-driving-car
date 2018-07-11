"""
Author: npgh2009
"""
 
import pygame, sys, random
from math import ceil
from pygame.locals import *
 
UP = 8
DOWN = 2
LEFT = 4
RIGHT = 6

#parameters
WALLWIDTH = 3
CHECKPOINTWIDTH = 1

def createCheckPoint(cp):
    #cp is a dictionary with keys 'x', 'y', 'dir', 'w(idth)', 'l(ength)'
    if cp['dir'] == DOWN:
        cprect = pygame.Rect(cp['x'], cp['y'], cp['w'], CHECKPOINTWIDTH)
        wall1 = pygame.Rect(cp['x']-WALLWIDTH, cp['y'], WALLWIDTH, cp['l'])
        wall2 = pygame.Rect(cp['x']+cp['w'], cp['y'], WALLWIDTH, cp['l'])
    elif cp['dir'] == UP:
        cprect = pygame.Rect(cp['x'], cp['y'], cp['w'], CHECKPOINTWIDTH)
        wall1 = pygame.Rect(cp['x']-WALLWIDTH, cp['y']-cp['l']+1, WALLWIDTH, cp['l'])
        wall2 = pygame.Rect(cp['x']+cp['w'], cp['y']-cp['l']+1, WALLWIDTH, cp['l'])
    elif cp['dir'] == LEFT:
        cprect = pygame.Rect(cp['x'], cp['y'], CHECKPOINTWIDTH, cp['w'])
        wall1 = pygame.Rect(cp['x']-cp['l']+1, cp['y']-WALLWIDTH, cp['l'], WALLWIDTH)
        wall2 = pygame.Rect(cp['x']-cp['l']+1, cp['y']+cp['w'], cp['l'], WALLWIDTH)
    else:
        cprect = pygame.Rect(cp['x'], cp['y'], CHECKPOINTWIDTH, cp['w'])
        wall1 = pygame.Rect(cp['x'], cp['y']-WALLWIDTH, cp['l'], WALLWIDTH)
        wall2 = pygame.Rect(cp['x'], cp['y']+cp['w'], cp['l'], WALLWIDTH)
       
    return cprect, wall1, wall2
 
#cpslist = [] #containing cp elements but without 'x', 'y' coordinate
 
def processCpsList(x, y, cpslist):
    #change the cpslist element, since input a list into function will only input pointer
    #add 'x', 'y' coordinate to the cp elements
    #and output a list of walls necessary for the drawing
    walls = []
    cpslist[0]['x'] = x
    cpslist[0]['y'] = y
   
    for i in range(1, len(cpslist)):
        c1 = cpslist[i] #CURRENT CHECKPOINT
        c0 = cpslist[i-1] #PREVIOUS CHECKPOINT
        
        if c1['dir'] == LEFT:
         
            if c0['dir'] == LEFT:
                if c0['w'] == c1['w']:
                    cpslist[i]['x'] = c0['x']-c0['l']
                    cpslist[i]['y'] = c0['y']
                else:
                    offset = ceil((c0['w']-c1['w'])/2)
                    cpslist[i]['x'] = c0['x']-c0['l']
                    cpslist[i]['y'] = c0['y']+offset
                    if offset > 0:
                        #walls.append(pygame.Rect(cpslist[i]['x']+1-WALLWIDTH, c0['y']-WALLWIDTH, WALLWIDTH, offset))
                        #walls.append(pygame.Rect(cpslist[i]['x']+1-WALLWIDTH, cpslist[i]['y']+c1['w']+WALLWIDTH, WALLWIDTH, c0['w']-offset-c1['w']))
                        wall1, wall2 = createRightToLeftShrink(cpslist[i]['y'], c0['y'], c1['w'], c0['w'], cpslist[i]['x'])
                    else:
                        wall1, wall2 = createLeftToRightShrink(cpslist[i]['y'], c0['y'], c1['w'], c0['w'], cpslist[i]['x'])
                    walls.append(wall1)
                    walls.append(wall2)
         
            elif c0['dir'] == RIGHT:
                raise ValueError
         
            elif c0['dir'] == DOWN:
                cpslist[i]['x'] = c0['x']-WALLWIDTH-1
                cpslist[i]['y'] = c0['y']+c0['l']
                wall1, wall2 = createBottomRightWall(c0['x']+c0['w']-1, c0['y']+c0['l']-1, cpslist[i]['x'], cpslist[i]['y']+c1['w']-1)
                walls.append(wall1)
                walls.append(wall2)
 
            elif c0['dir'] == UP:
                cpslist[i]['x'] = c0['x']-WALLWIDTH-1
                cpslist[i]['y'] = c0['y']-c0['l']+1-c1['w']
                wall1, wall2 = createTopRightWall(c0['x']+c0['w']-1, c0['y']-c0['l']+1, cpslist[i]['x'], cpslist[i]['y'])
                walls.append(wall1)
                walls.append(wall2)
 
        elif c1['dir'] == RIGHT:
 
            if c0['dir'] == LEFT:
                raise ValueError
           
            elif c0['dir'] == RIGHT:
                if c0['w'] == c1['w']:
                    cpslist[i]['x'] = c0['x']+c0['l']
                    cpslist[i]['y'] = c0['y']
                else:
                    offset = ceil((c0['w']-c1['w'])/2)
                    cpslist[i]['x'] = c0['x']+c0['l']
                    cpslist[i]['y'] = c0['y']+offset
                    if offset > 0:
                        wall1, wall2 = createLeftToRightShrink(c0['y'], cpslist[i]['y'], c0['w'], c1['w'], c0['x']+c0['l']-1)
                    else:
                        wall1, wall2 = createRightToLeftShrink(c0['y'], cpslist[i]['y'], c0['w'], c1['w'], c0['x']+c0['l']-1)
                    walls.append(wall1)
                    walls.append(wall2)

            elif c0['dir'] == DOWN:
                cpslist[i]['x'] = c0['x']+c0['w']+WALLWIDTH
                cpslist[i]['y'] = c0['y']+c0['l']
                wall1, wall2 = createBottomLeftWall(c0['x'], c0['y']+c0['l']-1, cpslist[i]['x'], cpslist[i]['y']+c1['w']-1)
                walls.append(wall1)
                walls.append(wall2)

            elif c0['dir'] == UP:
                cpslist[i]['x'] = c0['x']+c0['w']+WALLWIDTH
                cpslist[i]['y'] = c0['y']-c0['l']+1-c1['w']
                wall1, wall2 = createTopLeftWall(c0['x'], c0['y']-c0['l']+1, cpslist[i]['x'], cpslist[i]['y'])
                walls.append(wall1)
                walls.append(wall2)

        elif c1['dir'] == DOWN:

            if c0['dir'] == LEFT:
                cpslist[i]['x'] = c0['x']-c0['l']+1-WALLWIDTH-c1['w']
                cpslist[i]['y'] = c0['y']+c0['w']
                wall1, wall2 = createTopLeftWall(cpslist[i]['x'], cpslist[i]['y'], c0['x']-c0['l']+1, c0['y'])
                walls.append(wall1)
                walls.append(wall2)

            elif c0['dir'] == RIGHT:
                cpslist[i]['x'] = c0['x']+c0['l']+WALLWIDTH
                cpslist[i]['y'] = c0['y']+c0['w']
                wall1, wall2 = createTopRightWall(cpslist[i]['x']+c1['w']-1, cpslist[i]['y'], c0['x']+c0['l']-1, c0['y'])
                walls.append(wall1)
                walls.append(wall2)

            elif c0['dir'] == DOWN:
                if c0['w'] == c1['w']:
                    cpslist[i]['x'] = c0['x']
                    cpslist[i]['y'] = c0['y']+c0['l']
                else:
                    offset = ceil((c0['w']-c1['w'])/2)
                    cpslist[i]['x'] = c0['x']+offset
                    cpslist[i]['y'] = c0['y']+c0['l']
                    if offset > 0:
                        wall1, wall2 = createTopToBottomShrink(c0['x'], cpslist[i]['x'], c0['w'], c1['w'], c0['y']+c0['l']-1)
                    else:
                        wall1, wall2 = createBottomToTopShrink(c0['x'], cpslist[i]['x'], c0['w'], c1['w'], c0['y']+c0['l']-1)
                    walls.append(wall1)
                    walls.append(wall2)

            elif c0['dir'] == UP:
                raise ValueError

        elif c1['dir'] == UP:

            if c0['dir'] == LEFT:
                cpslist[i]['x'] = c0['x']-c0['l']+1-WALLWIDTH-c1['w']
                cpslist[i]['y'] = c0['y']-1
                wall1, wall2 = createBottomLeftWall(cpslist[i]['x'], cpslist[i]['y'], c0['x']-c0['l']+1, c0['y']+c0['w']-1)
                walls.append(wall1)
                walls.append(wall2)

            elif c0['dir'] == RIGHT:
                cpslist[i]['x'] = c0['x']+c0['l']+WALLWIDTH
                cpslist[i]['y'] = c0['y']-1
                wall1, wall2 = createBottomRightWall(cpslist[i]['x']+c1['w']-1, cpslist[i]['y'], c0['x']+c0['l']-1, c0['y']+c0['w']-1)
                walls.append(wall1)
                walls.append(wall2)

            elif c0['dir'] == DOWN:
                raise ValueError

            elif c0['dir'] == UP:
                if c0['w'] == c1['w']:
                    cpslist[i]['x'] = c0['x']
                    cpslist[i]['y'] = c0['y']-c0['l']
                else:
                    offset = ceil((c0['w']-c1['w'])/2)
                    cpslist[i]['x'] = c0['x']+offset
                    cpslist[i]['y'] = c0['y']-c0['l']
                    if offset > 0:
                        wall1, wall2 = createBottomToTopShrink(cpslist[i]['x'], c0['x'], c1['w'], c0['w'], cpslist[i]['y'])
                    else:
                        wall1, wall2 = createTopToBottomShrink(cpslist[i]['x'], c0['x'], c1['w'], c0['w'], cpslist[i]['y'])
                    walls.append(wall1)
                    walls.append(wall2)

    return walls


def createTopLeftWall(xl, yl, xt, yt):
    wall1 = pygame.Rect(xl-WALLWIDTH, yt-WALLWIDTH, xt-xl+WALLWIDTH, WALLWIDTH)
    wall2 = pygame.Rect(xl-WALLWIDTH, yt, WALLWIDTH, yl-yt)
    return wall1, wall2
 
def createBottomLeftWall(xl, yl, xb, yb):
    wall1 = pygame.Rect(xl-WALLWIDTH, yl+1, WALLWIDTH, yb-yl+WALLWIDTH)
    wall2 = pygame.Rect(xl-WALLWIDTH, yb+1, xb-xl+WALLWIDTH, WALLWIDTH)
    return wall1, wall2
 
def createTopRightWall(xr, yr, xt, yt):
    wall1 = pygame.Rect(xt+1, yt-WALLWIDTH, xr-xt+WALLWIDTH, WALLWIDTH)
    wall2 = pygame.Rect(xr+1, yt, WALLWIDTH, yr-yt)
    return wall1, wall2
 
def createBottomRightWall(xr, yr, xb, yb):
    wall1 = pygame.Rect(xb+1, yb+1, xr-xb+WALLWIDTH, WALLWIDTH)
    wall2 = pygame.Rect(xr+1, yr+1, WALLWIDTH, yb-yr)
    return wall1, wall2
 
def createRightToLeftShrink(yl, yr, wl, wr, xl):
    wall1 = pygame.Rect(xl+1-WALLWIDTH, yr-WALLWIDTH, WALLWIDTH, yl-yr)
    wall2 = pygame.Rect(xl+1-WALLWIDTH, yl+wl+WALLWIDTH, WALLWIDTH, wr-wl-(yl-yr))
    return wall1, wall2
 
def createLeftToRightShrink(yl, yr, wl, wr, xl):
    wall1 = pygame.Rect(xl+1, yl-WALLWIDTH, WALLWIDTH, yr-yl)
    wall2 = pygame.Rect(xl+1, yr+wr+WALLWIDTH, WALLWIDTH, wl-wr-(yr-yl))
    return wall1, wall2
 
def createTopToBottomShrink(xt, xb, wt, wb, yt):
    wall1 = pygame.Rect(xt-WALLWIDTH, yt+1, xb-xt, WALLWIDTH)
    wall2 = pygame.Rect(xb+wb+WALLWIDTH, yt+1, wt-wb-(xb-xt), WALLWIDTH) #wt-wb-xb-xt
    #wall2 = pygame.Rect(0,0,0,0)
    return wall1, wall2
 
def createBottomToTopShrink(xt, xb, wt, wb, yt):
    wall1 = pygame.Rect(xb-WALLWIDTH, yt+1-WALLWIDTH, xt-xb, WALLWIDTH)
    wall2 = pygame.Rect(xt+wt+WALLWIDTH, yt+1-WALLWIDTH, wb-wt-(xt-xb), WALLWIDTH)
    return wall1, wall2

def main():
    # set up pygame
    pygame.init()
    mainClock = pygame.time.Clock()

    # set up the window
    WINDOWWIDTH = 600
    WINDOWHEIGHT = 600
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('Race Track')

    # set up the colors
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    RED   = (255, 0, 0)
    BLUE  = (0, 0, 255)

    #set initial coordinate
    X0 = 50
    Y0 = 50

    #set track

    #counterclockwise
    # cpslist = [ {'dir': DOWN,  'w': 80, 'l': 200},
    #             {'dir': DOWN,  'w': 40, 'l': 200},
    #             {'dir': RIGHT, 'w': 70, 'l': 160},
    #             {'dir': RIGHT, 'w': 35, 'l': 160},
    #             {'dir': UP,    'w': 60, 'l': 140},
    #             {'dir': UP,    'w': 30, 'l': 140},
    #             {'dir': LEFT,  'w': 40, 'l': 120},
    #             {'dir': LEFT,  'w': 20, 'l': 120}]

    #clockwise
    cpslist = [ {'dir': RIGHT,  'w': 80, 'l': 200},
                {'dir': RIGHT,  'w': 40, 'l': 200},
                {'dir': DOWN, 'w': 70, 'l': 160},
                {'dir': DOWN, 'w': 35, 'l': 160},
                {'dir': LEFT,    'w': 60, 'l': 140},
                {'dir': LEFT,    'w': 30, 'l': 140},
                {'dir': UP,  'w': 40, 'l': 120},
                {'dir': UP,  'w': 20, 'l': 120}]

    while True:
        # check for the QUIT event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # draw the black background onto the surface
        windowSurface.fill(BLACK)           

        # create walls and checkpoints
        walls = processCpsList(X0, Y0, cpslist)
        cpsrect = []
        for cp in cpslist:
            cprect, wall1, wall2 = createCheckPoint(cp)
            walls.append(wall1)
            walls.append(wall2)
            cpsrect.append(cprect)

        # draw walls and checkpoints
        for i in range(len(walls)):
            pygame.draw.rect(windowSurface, GREEN, walls[i])
        for i in range(len(cpsrect)):
            pygame.draw.rect(windowSurface, BLUE, cpsrect[i])

        pygame.display.update()

if __name__ == "__main__":
    # execute only if run as a script
    main()