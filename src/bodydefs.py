from . import utils
from collections import namedtuple, deque


class Body:
    """
    Represents a celestial body.:
    Distance is measured in AU
        1 AU = 149,597,870.700 m
    Time is measured in years:
        1 yr = 31,557,600 s
    Mass is measured in solar masses, Ms:
        1 Ms = 4π2 AU^3/yr^3/G ≈ 1.99e30 kg
    Force is measured in F (arbitrary unit):
        1 F = G Ms^2 / AU^2 ≈ 2.989e23 N

    Parameters
    ----------
    pos : Vector2
        Initial position (in AU)
    vel : Vector2
        Initial velocity (in AU/yr)
    mass : float
        Mass (in solar masses)

    Attributes
    ----------
    pos : Vector2
    prev_pos : Vector2
    vel : Vector2
    prev_vel : Vector2
    forces : Vector2
    prev_forces : Vector2
    mass : float
    inv_mass : float
    """
    class State:
        """
        Gathers the information about the state of the
        body at a given time.
        """

        def __init__(self, pos, vel, forces):
            self.pos = pos
            self.vel = vel
            self.forces = forces

        def __str__(self):
            return "State({}, {}, {})".format(self.pos, self.vel, self.forces)

        def __repr__(self):
            return "<State: {}, {}, {}>".format(self.pos, self.vel,
                                                self.forces)

    def __init__(self, name, pos, vel, mass):
        self.name = name
        self.states = deque(maxlen=3)  # remember a few past states
        pos = utils.Vector2.from_pair(pos)
        vel = utils.Vector2.from_pair(vel)
        self.states.append(Body.State(pos, vel, utils.Vector2()))
        self.mass = mass
        self.inv_mass = 1 / mass

    @property
    def pos(self):
        return self.states[-1].pos

    @pos.setter
    def pos(self, new_pos):
        new_pos = utils.Vector2.from_pair(new_pos)
        self.states[-1].pos = new_pos

    @property
    def prev_pos(self):
        try:
            return self.states[-2].pos
        except IndexError:
            return self.pos

    @property
    def vel(self):
        return self.states[-1].vel

    @vel.setter
    def vel(self, new_vel):
        new_vel = utils.Vector2.from_pair(new_vel)
        self.states[-1].vel = new_vel

    @property
    def prev_vel(self):
        try:
            return self.states[-2].vel
        except IndexError:
            return self.vel

    @property
    def forces(self):
        return self.states[-1].forces

    @forces.setter
    def forces(self, new_forces):
        new_forces = utils.Vector2.from_pair(new_forces)
        self.states[-1].forces = new_forces

    @property
    def prev_forces(self):
        try:
            return self.states[-2].forces
        except IndexError:
            return self.forces

    def new_state(self):
        self.states.append(Body.State(self.pos, self.vel, utils.Vector2()))

    def apply_gravity_of(self, body):
        """Applies another body's gravitational force to this body."""
        r = self.pos - body.pos
        r3 = abs(r)**3
        self.forces += -(self.mass * body.mass / r3) * r

    def integrate(self, dt, method):
        self.vel, self.pos = method(self, dt)

    def __eq__(self, other):
        try:
            if self.name != other.name:
                return False
            if self.mass != other.mass:
                return False
            if self.pos != other.pos:
                return False
            if self.vel != other.vel:
                return False
        except AttributeError:
            return False
        else:
            return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, str(self))


class Planet(Body):
    pass


class Star(Body):
    pass
