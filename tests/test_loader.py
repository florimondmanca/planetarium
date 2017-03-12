import unittest

import src.loader as loader
from src.bodydefs import Planet


class TestLoader(unittest.TestCase):

    def test_readfile(self):
        lines = loader.readfile('planetfiles/test_readfile.planet')
        self.assertEqual(len(lines), 6)

    def test_get_creator(self):
        type_to_class = {
            'Planet': loader.PlanetCreator,
        }
        for bodytype in type_to_class:
            creator = loader.get_creator(bodytype)
            self.assertEqual(creator, type_to_class[bodytype])

    def test_creator_set(self):
        bodies = []
        with loader.PlanetCreator(bodies) as creator:
            creator.set('pos', (1, 2))
            creator.set('vel', (-3, 2))
            creator.set('name', 'Sun')
            creator.set('mass', 1)
        sun = Planet('Sun', (1, 2), (-3, 2), 1)
        self.assertEqual(sun, bodies[0])

    def test_parse_args(self):
        data = [
            ('pos: 34', 'pos', 34),
            ('name: Sun', 'name', 'Sun'),
            ('vel: (3, 4.5)', 'vel', (3, 4.5)),
            ('vel: (-2.3, 1.2)', 'vel', (-2.3, 1.2)),
            ('mass: 1.43', 'mass', 1.43),
        ]
        for line, exp_arg_name, exp_value in data:
            arg_name, value = loader.parse_args(line)
            self.assertEqual(arg_name, exp_arg_name)
            self.assertEqual(value, exp_value)

    def test_load_one_planet(self):
        bodies = loader.load('planetfiles/test_create_one_planet.planet')
        self.assertEqual(len(bodies), 1)
        planet = bodies[0]
        self.assertEqual(planet, Planet('Sun', (0, 2), (3, 1), 1))

    def test_load_multiple_planets(self):
        bodies = loader.load('planetfiles/test_create_n_planets.planet')
        self.assertEqual(len(bodies), 3)
        p1, p2, p3 = bodies
        self.assertEqual(p1, Planet('Sun', (0, 2), (3, 1), 1))
        self.assertEqual(p2, Planet('Earth', (-2, 1), (3, 4), 1))
        self.assertEqual(p3, Planet('Mars', (-5, -5), (10, 3), .5))
