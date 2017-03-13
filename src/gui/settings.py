import pygame
import random

pygame.font.init()


class SCREEN:
    WIDTH = 1200
    HEIGHT = 700
    SIZE = (WIDTH, HEIGHT)


class TIME:
    FPS = 30


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


class FONT:
    NAME = pygame.font.SysFont('arial', 10)
