import time

import pygame, sys
from pygame.locals import QUIT


HEIGHT = 700
WIDTH = 600
SPACE_WIDTH = 10

start = time.time()

def getTimeString():
    delta = time.time() - start;
    sec = delta % 60
    minutes = (delta / 60) % 60
    hours = (delta / (60 * 60)) % 24
    days = delta / (60 * 60 * 24)
    elapsed = {'days' : int(days), 'hours' : int(hours) , 'minutes' : int(minutes), 'sec' : int(sec)}
    return '%(days)sd%(hours)sh%(minutes)sm%(sec)ss' % elapsed;

def init():
    # set up pygame
    pygame.init()
    
    # set up the window
    windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Command list!')
    
    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # set up fonts
    basicFont = pygame.font.SysFont(None, 48)
    
    while True:
        # Rendering elapsed time
        elapsedTime = basicFont.render(getTimeString(), True, WHITE)
        elapsedTimeRect = elapsedTime.get_rect()
        elapsedTimeRect.centerx = WIDTH / 2 
        elapsedTimeRect.centery = elapsedTime.get_height() / 2 + SPACE_WIDTH*3
        
        # draw the black background onto the surface
        windowSurface.fill(BLACK)
    
        # get a pixel array of the surface
        pixArray = pygame.PixelArray(windowSurface)
        pixArray[480][380] = BLACK
        del pixArray
        
        # draw the elapsedTime onto the surface
        windowSurface.blit(elapsedTime, elapsedTimeRect)
        pygame.draw.line(windowSurface, WHITE, (0, 100), (WIDTH, 100), 4)
        
        # draw the window onto the screen
        pygame.display.update()
    
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
