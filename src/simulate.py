from . import loader
from . import methods
from . import bodydefs


class System:
    """
    Represents a system of bodies (stars, planets, etc.).

    Parameters
    ----------
    bodies : list of Body

    Attributes
    ----------
    bodies : list of Body
    """

    def __init__(self, bodies, integration_method=methods.Verlet):
        for body in bodies:
            if not isinstance(body, bodydefs.Body):
                raise TypeError('Expected Body, got {}: {}'
                                .format(body.__class__.__name__, body))
        self.bodies = list(bodies)
        self.method = integration_method
        self.dt = .01  # TODO: put it as parameter in .planet file
        self.step = 0

    def new_state(self):
        for body in self.bodies:
            body.new_state()

    def apply_gravity(self):
        for body in self.bodies:
            for other in self.others(body):
                body.apply_gravity_of(other)

    def others(self, current_body):
        for body in self.bodies:
            if body != current_body:
                yield body

    def integrate(self, dt, method):
        for body in self.bodies:
            body.integrate(dt, method=method)

    def update(self):
        self.apply_gravity()
        self.method.system_method(self, self.dt)
        self.new_state()
        self.step += 1

    def run(self, n_steps):
        for _ in range(n_steps):
            self.update()

    @staticmethod
    def from_file(planetfilename):
        return System(loader.load(planetfilename))
