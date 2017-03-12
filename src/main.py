class Body:

    def __init__(self, pos0, vel0, mass):
        self.pos = pos0
        self.vel = vel0
        self.mass = mass


class Planet(Body):
    pass


class Star(Body):
    pass
