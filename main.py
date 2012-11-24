import pygame
import sys
from pygame.locals import QUIT  # , MOUSE_MOTION, K_ESCAPE
from random import shuffle
import random
from square import Square
from time import sleep

WIDTH = 20
HEIGHT = 20
DELAY = 0.1

pygame.init()

clock = pygame.time.Clock()

windowSurfeceObj = pygame.display.set_mode((WIDTH * Square.SIZE, HEIGHT * Square.SIZE))
pygame.display.set_caption('Pymaze')


def drawPath(window, path):
    if len(path) == 0:
        return

    off = Square.SIZE / 2
    l = (path[0].x + off, path[0].y + off)

    for i in range(0, len(path)):
        sq = path[i]
        n = (sq.x * sq.SIZE + off, sq.y * sq.SIZE + off)
        pygame.draw.line(window, pygame.Color("black"), l, n, 3)
        l = n


def draw(window, grid, path):
    window.fill(pygame.Color("white"))
    for row in grid:
        for sq in row:
            sq.draw(window)
    drawPath(window, path)


def getNext(grid, sq, path):
    x = sq.x
    y = sq.y
    ret = []
    if x >= 1 and sq.check(grid[x - 1][y], "west", path):
        ret.append(grid[x - 1][y])
    if x < WIDTH - 1 and sq.check(grid[x + 1][y], "east", path):
        ret.append(grid[x + 1][y])
    if y >= 1 and sq.check(grid[x][y - 1], "north", path):
        ret.append(grid[x][y - 1])
    if y < HEIGHT - 1 and sq.check(grid[x][y + 1], "south", path):
        ret.append(grid[x][y + 1])

    if len(ret) == 0:
        return None
    else:
        return ret[random.randrange(len(ret))]


def breakIn(grid, sq):
    route = []
    while sq.path is False:
        route.append(sq)
        sq.current = True
        nextArr = []

        x = sq.x
        y = sq.y

        if x >= 1 and grid[x - 1][y].current is False:
            nextArr.append(grid[x - 1][y])
        if x < WIDTH - 1 and grid[x + 1][y].current is False:
            nextArr.append(grid[x + 1][y])
        if y >= 1 and grid[x][y - 1].current is False:
            nextArr.append(grid[x][y - 1])
        if y < HEIGHT - 1 and grid[x][y + 1].current is False:
            nextArr.append(grid[x][y + 1])

        if len(nextArr) is 0:
            sq = route[0]
            for r in route:
                r.current = False
            route = []
            return
        else:
            sq = nextArr[random.randrange(len(nextArr))]

        draw(windowSurfeceObj, grid, route)
        sleep(DELAY)
        pygame.display.update()

    route.append(sq)
    for i in range(1, len(route)):
        cur = route[i]
        cur.path = True
        cur.current = False
        cur.connectTo(route[i - 1])


def makeMaze():
    grid = [None] * WIDTH
    for x in range(0, WIDTH):
        grid[x] = [None] * HEIGHT
        for y in range(0, HEIGHT):
            grid[x][y] = Square(x, y)

    path = []
    current = grid[0][0]
    end = grid[len(grid) - 1][len(grid[0]) - 1]
    while current is not None:
        current.path = True
        path.append(current)
        if current == end:
            # getNext(current) # HACK HACK HACK!?
            break
        current = getNext(grid, current, path)
        while (len(path) != 0 and current is None):
            current = path[len(path) - 1]
            current = getNext(grid, current, path)
            if current is None:
                clear = path.pop()
                clear.north = clear.east = clear.south = clear.west = True
            draw(windowSurfeceObj, grid, path)
            sleep(DELAY)
            pygame.display.update()
        draw(windowSurfeceObj, grid, path)
        sleep(DELAY)
        pygame.display.update()
    for i in range(1, len(path)):
        cur = path[i]
        cur.connectTo(path[i - 1])

    for row in grid:
        for sq in row:
            sq.path = False
    for sq in path:
        sq.path = True
    for sq in path:
        x = sq.x
        y = sq.y
        if x >= 1 and grid[x - 1][y].path is False:
            sq.west = False
        if x < WIDTH - 1 and grid[x + 1][y].path is False:
            sq.east = False
        if y >= 1 and grid[x][y - 1].path is False:
            sq.north = False
        if y < HEIGHT - 1 and grid[x][y + 1].path is False:
            sq.south = False

    rem = []
    for row in grid:
        for sq in row:
            if sq.path is False:
                rem.append(sq)
                sq.north = sq.south = sq.east = sq.west = False
    shuffle(rem)

    while len(rem) > 0:
        cur = rem.pop()
        if cur.path is True:
            continue
        breakIn(grid, cur)

    return (grid, path)


done = makeMaze()
grid = done[0]
path = done[1]

Square.SHOW_PATH = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    draw(windowSurfeceObj, grid, path)
    pygame.display.update()
    clock.tick(60)
