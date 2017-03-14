import pygame
from . import settings
from ..core.simulate import System
from time import time


class Gui:

    def __init__(self, system):
        self.system = system
        self.screen = pygame.display.set_mode(settings.SCREEN.SIZE)
        self.clock = pygame.time.Clock()
        self.colors = {}
        self.names = {}
        for body in self.system.bodies:
            self.colors[body.name] = settings.COLORS.random()
        for body in self.system.bodies:
            name_image = settings.FONT.NAME.render(
                body.name, 1, self.colors[body.name])
            name_rect = name_image.get_rect()
            self.names[body.name] = (name_image, name_rect)

    def update(self):
        self.system.update()

    def draw(self):
        self.screen.fill(settings.COLORS.BLACK)
        for body in self.system.bodies:
            pygame.draw.circle(
                self.screen,
                self.colors[body.name],
                screen_coords(body.pos),
                screen_radius(body),
            )
            # pygame.draw.line(
            #     self.screen,
            #     settings.COLORS.RED,
            #     screen_coords(body.pos),
            #     screen_coords(body.pos + .1 * body.vel),
            # )
            pygame.draw.line(
                self.screen,
                settings.COLORS.GREEN,
                screen_coords(body.pos),
                screen_coords(body.pos + 1000 * body.prev_forces),
            )
            image, rect = self.names[body.name]
            rect.center = screen_coords(body.pos)
            rect.move_ip(0, -screen_radius(body) - 5)
            self.screen.blit(image, rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(settings.TIME.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for _ in range(settings.TIME.UPDATE_PER_FRAME):
                self.update()
            self.draw()

    @staticmethod
    def from_file(planetfilename):
        return Gui(System.from_file(planetfilename))


def screen_coords(vec):
    return (settings.SCREEN.WIDTH // 2 + int(50 * vec.x),
            settings.SCREEN.HEIGHT // 2 + int(-50 * vec.y))


def screen_radius(body):
    return int(10 * body.mass ** .1)
