import unittest

import src.loader as ld
from src.bodydefs import Planet


class TestLoader(unittest.TestCase):

    def test_readfile(self):
        lines = ld.Loader.readfile('planetfiles/test_readfile.planet')
        self.assertEqual(len(lines), 6)

    def test_get_creator(self):
        type_to_class = {
            'Planet': ld.PlanetCreator,
        }
        for bodytype in type_to_class:
            creator = ld.get_creator(bodytype)
            self.assertEqual(creator, type_to_class[bodytype])

    def test_creator_set(self):
        bodies = []
        with ld.PlanetCreator(bodies) as creator:
            creator.set('pos', (1, 2))
            creator.set('vel', (-3, 2))
            creator.set('name', 'Sun')
            creator.set('mass', 1)
        sun = Planet('Sun', (1, 2), (-3, 2), 1)
        self.assertEqual(sun, bodies[0])

    def test_parse_args(self):
        data = [
            ('pos: int: 34', 'pos', 34),
            ('name: str: Sun', 'name', 'Sun'),
            ('vel: tuple: (3, 4.5)', 'vel', (3, 4.5)),
            ('vel: tuple: (-2.3, 1.2)', 'vel', (-2.3, 1.2)),
            ('mass: float: 1.43', 'mass', 1.43),
        ]
        for line, exp_arg_name, exp_value in data:
            arg_name, value = ld.Loader.parse_args(line)
            self.assertEqual(arg_name, exp_arg_name)
            self.assertEqual(value, exp_value)

    # def test_create_planet(self):
    #     lines = ld.Loader.readfile('planetfiles/test_create_planet.planet')
    #     bodies = []
    #     with ld.get_creator('Planet')(bodies):
    #         line = ""
    #         while line != "END":
    #             line = lines.pop()
    #             arg_name, value = ld.Loader.parse_args(line)
