import pygame
from . import settings
from ..core.simulate import System


def screen_coords(vec):
    return (settings.SCREEN.CENTER[0] + int(settings.ZOOM.ZOOM * vec.x),
            settings.SCREEN.CENTER[1] + int(-settings.ZOOM.ZOOM * vec.y))


def screen_radius(body):
    return int(settings.ZOOM.ZOOM * settings.SCREEN_RADIUS.FACT *
               body.mass ** settings.SCREEN_RADIUS.EXP)


class Gui:

    def __init__(self, system):
        self.system = system
        self.screen = pygame.display.set_mode(settings.SCREEN.SIZE)
        self.clock = pygame.time.Clock()
        self.colors = {}
        self.names = {}
        self.init()

    def init(self):
        # attach color to body
        for body in self.system.bodies:
            self.colors[body.name] = settings.COLORS.random()
        # attach name to body
        for body in self.system.bodies:
            name_image = settings.FONT.NAME.render(
                body.name, 1, self.colors[body.name])
            name_rect = name_image.get_rect()
            self.names[body.name] = (name_image, name_rect)
        # make some starry background
        self.background = pygame.Surface(settings.SCREEN.SIZE)
        for _ in range(settings.BACKGROUND.NSTARS):
            pygame.draw.rect(self.background,
                             settings.COLORS.random_gray(),
                             ((settings.randx(), settings.randy()), (1, 1)))
        # draw first background
        self.draw_background()

    def update(self):
        self.system.update()

    def draw_background(self):
        self.screen.fill(settings.COLORS.BLACK)
        self.screen.blit(self.background, (0, 0))

    def draw_body(self, body):
        if not settings.DRAW.BODY:
            return
        pygame.draw.circle(
            self.screen,
            self.colors[body.name],
            screen_coords(body.pos),
            screen_radius(body),
        )

    def draw_vel(self, body):
        if not settings.DRAW.VEL:
            return
        pygame.draw.line(
            self.screen,
            settings.COLORS.RED,
            screen_coords(body.pos),
            screen_coords(body.pos + settings.ZOOM.VEL * body.vel),
        )

    def draw_forces(self, body):
        if not settings.DRAW.FORCES:
            return
        pygame.draw.line(
            self.screen,
            settings.COLORS.GREEN,
            screen_coords(body.pos),
            screen_coords(body.pos + settings.ZOOM.FORCES *
                          body.prev_forces),
        )

    def draw_name(self, body):
        if not settings.DRAW.NAMES:
            return
        image, rect = self.names[body.name]
        rect.center = screen_coords(body.pos)
        rect.move_ip(0, -screen_radius(body) - 10)
        self.screen.blit(image, rect)

    def draw(self):
        if settings.BACKGROUND.REDRAW:
            self.draw_background()
        for body in self.system.bodies:
            self.draw_body(body)
            self.draw_vel(body)
            self.draw_forces(body)
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
        return Gui(System.from_file(planetfilename))
