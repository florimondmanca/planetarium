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

    def update(self, system_method):
        self.apply_gravity()
        system_method(self, System.dt)
        self.new_state()
