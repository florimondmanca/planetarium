import pygame
from . import guiconfig
from .simulate import System


class Gui:

    def __init__(self, system):
        self.system = system
        self.screen = pygame.display.set_mode(guiconfig.SCREEN.SIZE)
        self.clock = pygame.time.Clock()
        self.colors = {}
        for body in self.system.bodies:
            self.colors[body.name] = guiconfig.COLORS.random()

    def update(self):
        self.system.update()

    def draw(self):
        self.screen.fill(guiconfig.COLORS.BLACK)
        for body in self.system.bodies:
            pygame.draw.circle(
                self.screen,
                self.colors[body.name],
                screen_coords(body.pos),
                screen_radius(body),
            )
            pygame.draw.line(
                self.screen,
                guiconfig.COLORS.RED,
                screen_coords(body.pos),
                screen_coords(body.pos + body.vel),
            )
            pygame.draw.line(
                self.screen,
                guiconfig.COLORS.GREEN,
                screen_coords(body.pos),
                screen_coords(body.pos + 1000 * body.prev_forces),
            )
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


def screen_coords(vec):
    return (guiconfig.SCREEN.WIDTH // 2 + int(200 * vec.x),
            guiconfig.SCREEN.HEIGHT // 2 + int(-200 * vec.y))


def screen_radius(body):
    return int(10 * body.mass ** .1)
