import pygame
from . import settings
from ..core.fast import generatesim, update
from ..fastparse.loader import load


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
        self.init()

    def init(self):
        # attach color to each body
        for body in len(self.data):
            self.colors.append(settings.COLORS.random())
        # attach name image to each body
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

    def draw_body(self, bidx, body):
        if not settings.DRAW.BODY:
            return
        pygame.draw.circle(
            self.screen,
            self.colors[bidx],
            screen_coords(body['pos']),
            screen_radius(body),
        )

    def draw_vel(self, bidx, body):
        if not settings.DRAW.VEL:
            return
        pygame.draw.line(
            self.screen,
            settings.COLORS.RED,
            screen_coords(body['pos']),
            screen_coords(body['pos'] + settings.ZOOM.VEL * body['vel']),
        )

    def draw_name(self, bidx, body):
        if not settings.DRAW.NAMES:
            return
        image, rect = self.names[bidx]
        rect.center = screen_coords(body['pos'])
        rect.move_ip(0, -screen_radius(body) - 10)
        self.screen.blit(image, rect)

    def draw(self):
        if settings.BACKGROUND.REDRAW:
            self.draw_background()
        for bidx, body in enumerate(self.data):
            self.draw_body(bidx, body)
            self.draw_vel(bidx, body)
            self.draw_name(bidx, body)
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
        names, bodies = zip(*result['bodies'])
        # config = result['config']
