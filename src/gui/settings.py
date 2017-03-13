import pygame
import random


class SCREEN:
    WIDTH = 800
    HEIGHT = 600
    SIZE = (WIDTH, HEIGHT)


class TIME:
    FPS = 60


class COLORS:
    BLACK = pygame.Color('#000000')
    RED = pygame.Color('#ff2222')
    GREEN = pygame.Color('#55ff55')

    @staticmethod
    def random():
        colorcode = '#'
        for _ in range(6):
            colorcode += random.choice('0123456789abcdef')
        return pygame.Color(colorcode)
