import unittest

import src.bodydefs as bodydefs


class TestBody(unittest.TestCase):

    def test_create_body(self):
        planet = bodydefs.Planet('Sun', (1, 2), (3, 4), 1)
        self.assertEqual(planet.name, 'Sun')
        self.assertEqual(planet.pos, (1, 2))
        self.assertEqual(planet.vel, (3, 4))
        self.assertEqual(planet.mass, 1)

    def test_str(self):
        planet = bodydefs.Planet('Sun', (1, 2), (3, 4), 1)
        self.assertEqual(str(planet), 'Sun')

    def test_repr(self):
        planet = bodydefs.Planet('Sun', (1, 2), (3, 4), 1)
        self.assertEqual(repr(planet), '<Planet: Sun>')

    def test_create_new_state(self):
        planet = bodydefs.Planet('Sun', (1, 2), (3, 4), 1)
        planet.forces = (4, 2)
        self.assertEqual(len(planet.states), 1)
        planet.new_state()
        planet.forces = (5, 3)
        self.assertEqual(len(planet.states), 2)
        self.assertEqual(planet.states[-2].pos, (1, 2))
        self.assertEqual(planet.states[-2].vel, (3, 4))
        self.assertEqual(planet.states[-2].forces, (4, 2))
        self.assertEqual(planet.states[-1].pos, (1, 2))
        self.assertEqual(planet.states[-1].vel, (3, 4))
        self.assertEqual(planet.states[-1].forces, (5, 3))

    def test_access_previous_pos(self):
        planet = bodydefs.Planet('Sun', (1, 2), (3, 4), 1)
        planet.new_state()
        planet.pos = (4, 2)
        self.assertEqual(planet.pos, (4, 2))
        self.assertEqual(planet.prev_pos, (1, 2))

    def test_access_previous_vel(self):
        planet = bodydefs.Planet('Sun', (1, 2), (3, 4), 1)
        planet.new_state()
        planet.vel = (4, 2)
        self.assertEqual(planet.vel, (4, 2))
        self.assertEqual(planet.prev_vel, (3, 4))

    def test_access_previous_forces(self):
        planet = bodydefs.Planet('Sun', (1, 2), (3, 4), 1)
        planet.forces = (0, 2)
        planet.new_state()
        planet.forces = (4, -1)
        self.assertEqual(planet.forces, (4, -1))
        self.assertEqual(planet.prev_forces, (0, 2))

    def test_equality_between_bodies(self):
        p1 = bodydefs.Planet('Earth', (0, 0), (0, 0), 1)
        p2 = bodydefs.Planet('Jupiter', (0, 0), (0, 0), 1)
        self.assertNotEqual(p1, p2)
        p3 = bodydefs.Planet('Earth', (0, 1), (0, 0), 1)
        self.assertNotEqual(p1, p3)
        p4 = bodydefs.Planet('Earth', (0, 0), (0, 1), 1)
        self.assertNotEqual(p1, p4)
        p5 = bodydefs.Planet('Earth', (0, 0), (0, 0), 20)
        self.assertNotEqual(p1, p5)
        same = bodydefs.Planet('Earth', (0, 0), (0, 0), 1)
        self.assertEqual(p1, same)

    def test_not_equal_with_nonbody(self):
        planet = bodydefs.Planet('Earth', (0, 0), (0, 0), 1)
        for other in (1, 'hello', (4, 2), True):
            self.assertNotEqual(planet, other)

    def test_apply_gravity(self):
        earth = bodydefs.Planet('Earth', (0, 0), (0, 0), 1)
        moon = bodydefs.Planet('Moon', (-3, 2), (4, 1), .1)
        self.assertEqual(abs(moon.forces), 0)
        moon.apply_gravity_of(earth)
        r = moon.pos - earth.pos
        r3 = abs(r) ** 3
        gravity = -(moon.mass * earth.mass / r3) * r
        self.assertGreater(gravity | (earth.pos - moon.pos), 0,
                           "Gravity is not attractive!")
        self.assertEqual(moon.forces, gravity)
