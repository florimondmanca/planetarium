import utils
import methods
from collections import namedtuple, deque

State = namedtuple('State', ['pos', 'vel', 'forces'])


class Body:
    """
    Represents a celestial body.
    Distances must be given in AU
        1 AU = 149,597,870.700 m
    Time is measured in years
        1 yr = 31,557,600 s
    Mass is measured in solar masses, Ms
        1 Ms = 4π2 AU^3/yr^3/G ≈ 1.99e30 kg
    Force is measured in F (arbitrary unit)
        1 F = G Ms^2 / AU^2 ≈ 2.989e23 N

    Parameters
    ----------
    pos0 : Vector2
        Initial position (in AU)
    vel0 : Vector2
        Initial velocity (in AU/yr)
    mass : float
        Mass (in solar masses)

    Attributes
    ----------
    pos : Vector2
    vel : Vector2
    mass : float
    inv_mass : float
    forces : Vector2
        The forces applied to the Body.
    """

    def __init__(self, pos0, vel0, mass):
        self.states = deque(maxlen=3)
        self.states.appendleft(State(pos0, vel0, utils.Vector2()))
        self.mass = mass
        self.inv_mass = 1 / mass

    @property
    def pos(self):
        return self.states[-1].pos

    @property
    def prev_pos(self):
        return self.states[-2].pos

    @property
    def vel(self):
        return self.states[-1].vel

    @property
    def forces(self):
        return self.states[-1].forces

    @property
    def prev_forces(self):
        return self.states[-2].forces

    def new_state(self):
        self.states.appendleft(State(self.pos, self.vel, utils.Vector2()))

    def apply_gravity(self, body):
        """Applies another body's gravitational force to this body."""
        r = body.pos - self.pos
        r3 = abs(r)**3
        gravity = -(body.mass / r3) * r
        self.forces += -(self.mass * body.mass / r3) * r

    def integrate(self, dt, method=methods.euler):
        self.vel, self.pos = method(self, dt)


class Planet(Body):
    pass


class Star(Body):
    pass


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
        self.bodies = list(bodies)

    @staticmethod
    def load(planetfile):
        """
        Loads a System defined in a .planet file.
        """
        pass

    def new_state(self):
        for body in self.bodies:
            body.new_state()

    def apply_gravity(self):
        for body in self.bodies:
            for other in self.others(body):
                body.apply_gravity(other)

    def others(self, somebody):
        for body in self.bodies:
            if body != somebody:
                yield body

    def integrate(self, body_method):
        for body in self.bodies:
            body.integrate(System.dt, method=body_method)

    def update(self, system_method):
        self.apply_gravity()
        method(system, dt)
        system.new_state()
