import unittest
import src.core.methods as methods
from tests.utils import randscalar, randtuple
from src.core.bodydefs import Body
import numpy as np


class TestMethods(unittest.TestCase):

    def test_euler_raw_method(self):
        at, vt, xt, dt = randscalar(), randscalar(), randscalar(), .1
        vtpdt, xtpdt = methods.Euler.raw_method(at, vt, xt, dt)
        self.assertEqual(vtpdt, vt + at * dt)
        self.assertEqual(xtpdt, xt + vt * dt)

    def test_euler_body_method(self):
        x = randtuple()
        v = randtuple()
        f = randtuple()
        body = Body('TestBody', x, v, 1)
        body.forces = f
        dt = .1
        xt = np.array(x)
        vt = np.array(v)
        at = np.array(f) * body.inv_mass
        body.integrate(dt, methods.Euler.body_method)
        self.assertEqual(body.pos, xt + vt * dt)
        self.assertEqual(body.vel, vt + at * dt)

    def test_verlet_body_method(self):
        # setup
        x = randtuple()
        v = randtuple()
        ft = randtuple()
        body = Body('TestBody', x, v, 1)
        body.new_state()  # Verlet needs at least 1 step
        body.forces = ft
        dt = .1
        xt = np.array(x)
        vt = np.array(v)
        at = np.array(ft) * body.inv_mass
        # first part of integration: position
        xtpdt = xt + vt * dt + 1 / 2 * at * dt**2
        ftpdt = randtuple()
        atpdt = np.array(ftpdt) * body.inv_mass
        body.integrate(dt, methods.Verlet.body_method_pos)
        self.assertEqual(body.vel, v)
        self.assertEqual(body.pos, xtpdt)
        # second part of integration: velocity
        body.new_state()
        body.forces = ftpdt
        self.assertEqual(body.forces, ftpdt)
        self.assertEqual(body.prev_forces, ft)
        body.integrate(dt, methods.Verlet.body_method_vel)
        self.assertEqual(body.pos, xtpdt)
        self.assertEqual(body.vel, vt + (at + atpdt) / 2 * dt)


if __name__ == '__main__':
    unittest.main()
