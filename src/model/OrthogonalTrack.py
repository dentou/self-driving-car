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
CHECKPOINTHITBOX = 3
CHECKPOINTSTEP = 5

class OrthogonalTrack(object):
    def __init__(self, checkpointlist, X0, Y0):
        """
        Input:  list of track checkpoints, including 'dir', 'w'(idth) and 'l'(ength)
                X0, Y0: start place
        Example:
        cpslist = [ {'dir': RIGHT,  'w': 80, 'l': 200},
                    {'dir': RIGHT,  'w': 40, 'l': 200},
                    {'dir': DOWN, 'w': 70, 'l': 160},
                    {'dir': DOWN, 'w': 35, 'l': 160},
                    {'dir': LEFT,    'w': 60, 'l': 140},
                    {'dir': LEFT,    'w': 30, 'l': 140},
                    {'dir': UP,  'w': 40, 'l': 120},
                    {'dir': UP,  'w': 20, 'l': 120}]

        Output is self.walls and self.checkpoints, each containing pygame.Rect object
        """
        self.walls = processCpsList(X0, Y0, checkpointlist)
        self.checkpoints = []
        self.checkpointshitbox = []
        for cp in checkpointlist:
            cprect, cprecthitbox, wall1, wall2 = createCheckPoint(cp)
            #cprect, wall1, wall2 = createCheckPoint(cp)
            self.walls.append(wall1)
            self.walls.append(wall2)
            self.checkpoints += cprect
            self.checkpointshitbox += cprecthitbox

    def addWall(self, x, y, dir, length):
        if dir == DOWN:
            self.walls.append(pygame.Rect(x, y, WALLWIDTH, length))
        elif dir == RIGHT:
            self.walls.append(pygame.Rect(x, y, length, WALLWIDTH))

    def addCheckPoint(self, x, y, dir, length):
        if dir == DOWN:
            self.checkpoints.append(pygame.Rect(x, y, CHECKPOINTWIDTH, length))
            self.checkpointshitbox.append(pygame.Rect(x, y, CHECKPOINTHITBOX, length))
        elif dir == RIGHT:
            self.checkpoints.append(pygame.Rect(x, y, length, CHECKPOINTWIDTH))
            self.checkpointshitbox.append(pygame.Rect(x, y, length, CHECKPOINTHITBOX))

def createCheckPoint(cp):
    #cp is a dictionary with keys 'x', 'y', 'dir', 'w(idth)', 'l(ength)'
    cprect = []
    cprecthitbox = []
    
    if cp['dir'] == DOWN:
        pos = cp['y']
        while pos < (cp['y'] + cp['l']):
            cprect.append(pygame.Rect(cp['x'], pos, cp['w'], CHECKPOINTWIDTH))
            cprecthitbox.append(pygame.Rect(cp['x'], pos, cp['w'], CHECKPOINTHITBOX))
            pos += CHECKPOINTSTEP
        #cprect = pygame.Rect(cp['x'], cp['y'], cp['w'], CHECKPOINTWIDTH)
        #cprecthitbox = pygame.Rect(cp['x'], cp['y'], cp['w'], CHECKPOINTHITBOX)
        wall1 = pygame.Rect(cp['x']-WALLWIDTH, cp['y'], WALLWIDTH, cp['l'])
        wall2 = pygame.Rect(cp['x']+cp['w'], cp['y'], WALLWIDTH, cp['l'])
    
    elif cp['dir'] == UP:
        pos = cp['y']
        while pos > (cp['y'] - cp['l']):
            cprect.append(pygame.Rect(cp['x'], pos, cp['w'], CHECKPOINTWIDTH))
            cprecthitbox.append(pygame.Rect(cp['x'], pos, cp['w'], CHECKPOINTHITBOX))
            pos -= CHECKPOINTSTEP
        #cprect = pygame.Rect(cp['x'], cp['y'], cp['w'], CHECKPOINTWIDTH)
        #cprecthitbox = pygame.Rect(cp['x'], cp['y'], cp['w'], CHECKPOINTHITBOX)
        wall1 = pygame.Rect(cp['x']-WALLWIDTH, cp['y']-cp['l']+1, WALLWIDTH, cp['l'])
        wall2 = pygame.Rect(cp['x']+cp['w'], cp['y']-cp['l']+1, WALLWIDTH, cp['l'])
    
    elif cp['dir'] == LEFT:
        pos = cp['x']
        while pos > (cp['x'] - cp['l']):
            cprect.append(pygame.Rect(pos, cp['y'], CHECKPOINTWIDTH, cp['w']))
            cprecthitbox.append(pygame.Rect(pos, cp['y'], CHECKPOINTHITBOX, cp['w']))
            pos -= CHECKPOINTSTEP
        #cprect = pygame.Rect(cp['x'], cp['y'], CHECKPOINTWIDTH, cp['w'])
        #cprecthitbox = pygame.Rect(cp['x'], cp['y'], CHECKPOINTHITBOX, cp['w'])
        wall1 = pygame.Rect(cp['x']-cp['l']+1, cp['y']-WALLWIDTH, cp['l'], WALLWIDTH)
        wall2 = pygame.Rect(cp['x']-cp['l']+1, cp['y']+cp['w'], cp['l'], WALLWIDTH)
    
    else: #cp['dir'] == RIGHT
        pos = cp['x']
        while pos < (cp['x'] + cp['l']):
            cprect.append(pygame.Rect(pos, cp['y'], CHECKPOINTWIDTH, cp['w']))
            cprecthitbox.append(pygame.Rect(pos, cp['y'], CHECKPOINTHITBOX, cp['w']))
            pos += CHECKPOINTSTEP
        #cprect = pygame.Rect(cp['x'], cp['y'], CHECKPOINTWIDTH, cp['w'])
        #cprecthitbox = pygame.Rect(cp['x'], cp['y'], CHECKPOINTHITBOX, cp['w'])
        wall1 = pygame.Rect(cp['x'], cp['y']-WALLWIDTH, cp['l'], WALLWIDTH)
        wall2 = pygame.Rect(cp['x'], cp['y']+cp['w'], cp['l'], WALLWIDTH)
       
    return cprect, cprecthitbox, wall1, wall2
    #return cprect, wall1, wall2
 
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
    return wall1, wall2
 
def createBottomToTopShrink(xt, xb, wt, wb, yt):
    wall1 = pygame.Rect(xb-WALLWIDTH, yt+1-WALLWIDTH, xt-xb, WALLWIDTH)
    wall2 = pygame.Rect(xt+wt+WALLWIDTH, yt+1-WALLWIDTH, wb-wt-(xt-xb), WALLWIDTH)
    return wall1, wall2



def trackTemplate1(X0, Y0):
    #clockwise
    cpslist = [ {'dir': RIGHT,  'w': 80, 'l': 200},
                {'dir': RIGHT,  'w': 40, 'l': 200},
                {'dir': DOWN, 'w': 70, 'l': 160},
                {'dir': DOWN, 'w': 35, 'l': 160},
                {'dir': LEFT,    'w': 60, 'l': 140},
                {'dir': LEFT,    'w': 30, 'l': 140},
                {'dir': UP,  'w': 40, 'l': 120},
                {'dir': UP,  'w': 20, 'l': 120}]
    return OrthogonalTrack(cpslist, X0, Y0)

def trackTemplate2(X0, Y0):
    cpslist = [ {'dir': RIGHT,  'w': 100, 'l': 200},
            {'dir': RIGHT,  'w': 60, 'l': 200},
            {'dir': DOWN, 'w': 70, 'l': 160},
            {'dir': DOWN, 'w': 55, 'l': 160},
            {'dir': LEFT,    'w': 70, 'l': 140},
            {'dir': LEFT,    'w': 50, 'l': 140},
            {'dir': UP,  'w': 60, 'l': 120},
            {'dir': UP,  'w': 45, 'l': 120}]

    track = OrthogonalTrack(cpslist, X0, Y0)
    track.addWall(X0 - WALLWIDTH, Y0 - WALLWIDTH, DOWN, WALLWIDTH*2 + cpslist[0]['w'])

    return track

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

    # #clockwise
    # cpslist = [ {'dir': RIGHT,  'w': 80, 'l': 200},
    #             {'dir': RIGHT,  'w': 40, 'l': 200},
    #             {'dir': DOWN, 'w': 70, 'l': 160},
    #             {'dir': DOWN, 'w': 35, 'l': 160},
    #             {'dir': LEFT,    'w': 60, 'l': 140},
    #             {'dir': LEFT,    'w': 30, 'l': 140},
    #             {'dir': UP,  'w': 40, 'l': 120},
    #             {'dir': UP,  'w': 20, 'l': 120}]

    #create track
    track = trackTemplate2(X0, Y0)

    while True:
        # check for the QUIT event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # draw the black background onto the surface
        windowSurface.fill(BLACK)           

        # draw walls and checkpoints
        for i in range(len(track.walls)):
            pygame.draw.rect(windowSurface, GREEN, track.walls[i])
        for i in range(len(track.checkpoints)):
            pygame.draw.rect(windowSurface, BLUE, track.checkpoints[i])

        pygame.display.update()

if __name__ == "__main__":
    # execute only if run as a script
    main()