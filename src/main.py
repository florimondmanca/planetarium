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

    def others(self, somebody):
        for body in self.bodies:
            if body != somebody:
                yield body

    def update(self):
        # apply forces
        for body in self.bodies:
            for other in self.others(body):
                body.apply_gravity(other)
        # integrate laws of motion
        for body in self.bodies:
            body.integrate()
        # reset forces
        for body in self.bodies:
            body.reset_forces()
