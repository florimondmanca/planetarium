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
        self.assertEqual(len(planet.states), 1)
        planet.new_state()
        self.assertEqual(len(planet.states), 2)
        self.assertEqual(planet.pos, planet.prev_pos)
        self.assertEqual(planet.vel, planet.prev_vel)

    def test_access_previous_properties(self):
        planet = bodydefs.Planet('Sun', (1, 2), (3, 4), 1)
        planet.new_state()
        planet.pos = (5, 6)
        planet.vel = (7, 8)
        self.assertEqual(planet.pos, (5, 6))
        self.assertEqual(planet.prev_pos, (1, 2))
        self.assertEqual(planet.vel, (7, 8))
        self.assertEqual(planet.prev_vel, (3, 4))

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
        r = earth.pos - moon.pos
        r3 = abs(r) ** 3
        gravity = -(moon.mass * earth.mass / r3) * r
        self.assertEqual(moon.forces, gravity)
