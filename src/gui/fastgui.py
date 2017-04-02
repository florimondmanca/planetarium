import pygame
from . import settings
from ..core.fast import generatesim, update
from ..parse.loader import load


def screen_coords(vec):
    return (settings.SCREEN.CENTER[0] + int(settings.ZOOM.ZOOM * vec.x),
            settings.SCREEN.CENTER[1] + int(-settings.ZOOM.ZOOM * vec.y))


def screen_radius(b):
    return int(settings.ZOOM.ZOOM * settings.SCREEN_RADIUS.FACT *
               b['mass'] ** settings.SCREEN_RADIUS.EXP)


class Gui:

    def __init__(self, first_state, names):
        self.data = first_state
        self.str_names = names
        self.names = []
        self.colors = []
        self.screen = pygame.display.set_mode(settings.SCREEN.SIZE)
        self.clock = pygame.time.Clock()
        self.colors = []
        self.init()

    def init(self):
        # attach color to each body
        for body in len(self.data):
            self.colors.append(settings.COLORS.random())
        # attach name to each body
        for body in len(self.data):
            name_image = settings.FONT.NAME.render(
                self.str_names[body], 1,
                self.colors[body])
            name_rect = name_image.get_rect()
            self.names.append((name_image, name_rect))
        # make some starry background
        self.background = pygame.Surface(settings.SCREEN.SIZE)
        for _ in range(settings.BACKGROUND.NSTARS):
            pygame.draw.rect(self.background,
                             settings.COLORS.random_gray(),
                             ((settings.randx(), settings.randy()), (1, 1)))
        # draw first background
        self.draw_background()

    def update(self):
        self.data = update(self.data, .01)

    def draw_background(self):
        self.screen.fill(settings.COLORS.BLACK)
        self.screen.blit(self.background, (0, 0))

    def draw_body(self, body):
        if not settings.DRAW.BODY:
            return
        b = self.data[body]
        pygame.draw.circle(
            self.screen,
            self.colors[body],
            screen_coords(b['pos']),
            screen_radius(b),
        )

    def draw_vel(self, body):
        if not settings.DRAW.VEL:
            return
        b = self.data[body]
        pygame.draw.line(
            self.screen,
            settings.COLORS.RED,
            screen_coords(b['pos']),
            screen_coords(b['pos'] + settings.ZOOM.VEL * b['vel']),
        )

    def draw_name(self, body):
        if not settings.DRAW.NAMES:
            return
        b = self.data[body]
        image, rect = self.names[body]
        rect.center = screen_coords(b['pos'])
        rect.move_ip(0, -screen_radius(b) - 10)
        self.screen.blit(image, rect)

    def draw(self):
        if settings.BACKGROUND.REDRAW:
            self.draw_background()
        for body in len(self.data):
            self.draw_body(body)
            self.draw_vel(body)
            self.draw_name(body)
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
        result = load(planetfilename)
