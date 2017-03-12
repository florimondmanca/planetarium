import utils


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
    forces : Vector2
        The forces applied to the Body.
    """

    def __init__(self, pos0, vel0, mass):
        self.pos = pos0
        self.vel = vel0
        self.mass = mass
        self.forces = utils.Vector2()


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

    def __init__(self, *bodies):
        self.bodies = list(bodies)

    def update(self):
        pass
