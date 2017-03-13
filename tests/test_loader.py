import unittest

import src.loader as loader
from src.bodydefs import Planet


class TestLoader(unittest.TestCase):

    def test_readfile(self):
        lines = loader.readfile('planetfiles/test_readfile.planet')
        self.assertEqual(len(lines), 6)

    def test_read_nonexisting_file_raises_exception(self):
        with self.assertRaises(FileNotFoundError):
            loader.readfile('planetfiles/non_existing.planet')

    def test_get_creator(self):
        type_to_class = {
            'Planet': loader.PlanetCreator,
            'Star': loader.StarCreator,
            'System': loader.SystemCreator,
        }
        for bodytype in type_to_class:
            creator = loader.get_creator(bodytype)
            self.assertIsInstance(creator, type_to_class[bodytype])

    def test_creator_set_method(self):
        with loader.get_creator('Planet') as creator:
            creator.set('pos', (1, 2))
            creator.set('vel', (-3, 2))
            creator.set('name', 'Sun')
            creator.set('mass', 1)
        result = creator.get()
        bodies = result['bodies']()
        sun = Planet('Sun', (1, 2), (-3, 2), 1)
        self.assertEqual(sun, bodies[0])

    def test_parse_valid_args(self):
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

    def test_parse_unknown_args_raises_exception(self):
        data = [
            ('posa: 34', 'pos', 34),
            ('namex: Sun', 'name', 'Sun'),
            ('vel0: (3, 4.5)', 'vel', (3, 4.5)),
            ('haha: (-2.3, 1.2)', 'vel', (-2.3, 1.2)),
            ('mass1: 1.43', 'mass', 1.43),
        ]
        for line, exp_arg_name, exp_value in data:
            with self.assertRaises(TypeError):
                loader.parse_args(line)

    def test_load_missing_arg_raises_exception(self):
        with self.assertRaises(ValueError) as cm:
            with loader.get_creator('Planet') as creator:
                creator.set('name', 'Sun')
                creator.set('pos', (0, 2))
                # vel missing
                creator.set('mass', 1)
        self.assertIn("missing", str(cm.exception))

    def test_parse_mistyped_declaration_raises_exception(self):
        data = [
            ('pos, 34', 'pos', 34),
            ('name=Sun', 'name', 'Sun'),
            ('vel (3, 4.5)', 'vel', (3, 4.5)),
            ('mass -> 1.43', 'mass', 1.43),
        ]
        for line, exp_arg_name, exp_value in data:
            with self.assertRaises(SyntaxError) as cm:
                loader.parse_args(line)
            self.assertIn("mistyped", str(cm.exception),
                          "insufficient exception cause information")

    def test_load_missing_end_raises_exception(self):
        lines = loader.Lines([
            "PLANET",
            "name: Sun",
            "pos: (0, 2)",
            "vel: (0, 3)",
            "mass: 1",
            "PLANET",
        ])
        with self.assertRaises(SyntaxError) as cm:
            loader.load_from_lines_object(lines)
        self.assertIn("END statement", str(cm.exception),
                      "insufficient exception cause information")

    def test_load_one_planet(self):
        result = loader.load('planetfiles/test_create_one_planet.planet')
        bodies = result['bodies']
        self.assertEqual(len(bodies), 1)
        planet = bodies[0]
        self.assertEqual(planet, Planet('Sun', (0, 2), (3, 1), 1))

    def test_load_multiple_planets(self):
        result = loader.load('planetfiles/test_create_n_planets.planet')
        bodies = result['bodies']
        self.assertEqual(len(bodies), 3)
        p1, p2, p3 = bodies
        self.assertEqual(p1, Planet('Sun', (0, 2), (3, 1), 1))
        self.assertEqual(p2, Planet('Earth', (-2, 1), (3, 4), 1))
        self.assertEqual(p3, Planet('Mars', (-5, -5), (10, 3), .5))
