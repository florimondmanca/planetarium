import unittest

import src.bodydefs as bodydefs


class TestBody(unittest.TestCase):

    def test_create_body(self):
        planet = bodydefs.Planet('Sun', (1, 2), (3, 4), 1)
        self.assertEqual(planet.name, 'Sun')
        self.assertEqual(planet.pos, (1, 2))
        self.assertEqual(planet.vel, (3, 4))
        self.assertEqual(planet.mass, 1)
