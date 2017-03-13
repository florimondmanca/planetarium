import pygame
from . import guiconfig
from .simulate import System


class Gui:

    def __init__(self, system):
        self.system = system
        self.screen = pygame.display.set_mode(guiconfig.SCREEN.SIZE)
        self.clock = pygame.time.Clock()

    def update(self):
        self.system.update()

    def draw(self):
        self.screen.fill(guiconfig.COLORS.BLACK)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(guiconfig.TIME.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            self.draw()

    @staticmethod
    def from_file(planetfilename):
        return Gui(System.from_file(planetfilename))
