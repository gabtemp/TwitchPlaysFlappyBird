import time

import pygame, sys
from pygame.locals import QUIT


start = time.time()

def getTimeString():
    delta = time.time() - start;
    sec = (delta) % 60
    minutes = ((delta / 60) % 60)
    hours = ((delta / (60 * 60)) % 24);
    days = ((delta / (60 * 60)) / 24)
    elapsed = {'days' : int(days), 'hours' : int(hours) , 'minutes' : int(minutes), 'sec' : int(sec)}
    return '%(days)sd%(hours)sh%(minutes)sm%(sec)ss' % elapsed;

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((500, 800), 0, 32)
pygame.display.set_caption('Command list!')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set up fonts
basicFont = pygame.font.SysFont(None, 48)

while True:
    # Rendering elapsed time
    text = basicFont.render(getTimeString(), True, WHITE)
    textRect = text.get_rect()
    textRect.centerx = text.get_width()/2 + 5
    textRect.centery = text.get_height()/2 + 5
    
    # draw the white background onto the surface
    windowSurface.fill(BLACK)
    
    # get a pixel array of the surface
    pixArray = pygame.PixelArray(windowSurface)
    pixArray[480][380] = BLACK
    del pixArray
    
    # draw the text onto the surface
    windowSurface.blit(text, textRect)
    
    # draw the window onto the screen
    pygame.display.update()

    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
