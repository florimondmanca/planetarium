import pygame
import random

pygame.font.init()


class SCREEN:
    WIDTH = 1200
    HEIGHT = 700
    HALF_WIDTH = WIDTH // 2
    HALF_HEIGHT = HEIGHT // 2
    CENTER = (HALF_WIDTH, HALF_HEIGHT)
    SIZE = (WIDTH, HEIGHT)


class TIME:
    FPS = 30
    UPDATE_PER_FRAME = 2  # effective fps ≈ 1 / (.01 + .012 * this)


class COLORS:
    BLACK = pygame.Color('#000000')
    WHITE = pygame.Color('#ffffff')
    RED = pygame.Color('#ff2222')
    GREEN = pygame.Color('#55ff55')

    @staticmethod
    def random():
        colorcode = '#'
        for _ in range(6):
            colorcode += random.choice('0123456789abcdef')
        return pygame.Color(colorcode)

    @staticmethod
    def random_gray():
        gray = int(255 * random.random()**3)
        return pygame.Color(gray, gray, gray)


class ZOOM:
    ZOOM = 20
    VEL = 0.1
    FORCES = 1000


class SCREEN_RADIUS:
    FACT = .25
    EXP = 0.15


class FONT:
    NAME = pygame.font.SysFont('arial', 10)


class BACKGROUND:
    REDRAW = True
    NSTARS = int(1e5 / ZOOM.ZOOM)


class DRAW:
    BODY = True
    NAMES = True
    VEL = False
    FORCES = False


def randx():
    return int(random.random() * SCREEN.WIDTH)


def randy():
    return int(random.random() * SCREEN.HEIGHT)
