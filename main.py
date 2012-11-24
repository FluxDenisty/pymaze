import pygame
import sys
from pygame.locals import QUIT  # , MOUSE_MOTION, K_ESCAPE

import Square

def draw(window, grid):
    window.fill(pygame.color.white)
    for row in grid:
        for sq in row:
            sq.draw()

def drawPath(window, path):
    off = Square.SIZE / 2

    for sq in path:



pygame.init()
clock = pygame.time.Clock()

WIDTH = 64
HEIGHT = 64


windowSurfeceObj = pygame.display.set_mode((WIDTH * Square.SIZE, HEIGHT * Square.SIZE))
pygame.display.set_caption('Pymaze')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    draw(windowSurfeceObj, grid);
    pygame.display.update()
    clock.tick(60)
