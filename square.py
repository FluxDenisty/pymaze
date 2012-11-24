import pygame


class Square:

    SIZE = 10
    SHOW_PATH = True

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.north = False
        self.south = False
        self.east = False
        self.west = False
        self.path = False
        self.current = False

    def draw(self, window):
        red = pygame.color.red

        if (Square.SHOW_PATH and self.path):
            box = (self.x, self.y, self.SIZE, self.SIZE)
            pygame.draw.rect(window, pygame.color.blue, box, 0)

        f = (self.x, self.y)
        t = (self.x + self.SIZE, self.y)

        if (not self.north):
            pygame.draw.line(window, red, f, t)

        f = t
        t = (self.x + self.SIZE, self.y + self.SIZE)

        if (not self.east):
            pygame.draw.line(window, red, f, t)

        f = t
        t = (self.x, self.y + self.SIZE)

        if (not self.south):
            pygame.draw.line(window, red, f, t)

        f = t
        t = (self.x, self.y)

        if (not self.west):
            pygame.draw.line(window, red, f, t)

    def check(self, sq, fr, path):
        if sq is None:
            return False

        if sq.path:
            if (sq != path[path.len - 2]):
                setattr(self, fr, False)
            return False

        return True

    def connectTo(self, sq):
        if sq is None:
            return

        if sq.x < self.x:
            self.west = sq.east = True
        elif sq.x > self.x:
            self.east = sq.west = True
        elif sq.y < self.y:
            self.north = sq.south = True
        elif sq.y > self.y:
            self.south = sq.north = True
        else:
            print "WAT? in connectTo at %i, %i" % (self.x, self.y)
