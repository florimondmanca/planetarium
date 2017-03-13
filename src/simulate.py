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
    dt = 1e-3

    def __init__(self, *bodies):
        for body in bodies:
            if not isinstance(body, bodydefs.Body):
                raise TypeError('Expected Body, got {}: {}'
                                .format(body.__class__.__name__, body))
        self.bodies = list(bodies)

    def new_state(self):
        for body in self.bodies:
            body.new_state()

    def apply_gravity(self):
        for body in self.bodies:
            for other in self.others(body):
                body.apply_gravity(other)

    def others(self, current_body):
        for body in self.bodies:
            if body != current_body:
                yield body

    def integrate(self, body_method):
        for body in self.bodies:
            body.integrate(System.dt, method=body_method)

    def update(self, dt, system_method):
        self.apply_gravity()
        system_method(self, dt)
        self.new_state()

    def run(self, dt, n_steps):
        for _ in range(n_steps):
            self.update(dt, methods.euler)

    @staticmethod
    def from_file(planetfilename):
        return System(loader.load(planetfilename))
