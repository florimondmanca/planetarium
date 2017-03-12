import unittest

from src.utils import Vector2


class TestVector2(unittest.TestCase):

    def test_create_null_vector(self):
        v = Vector2()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)


if __name__ == '__main__':
    unittest.main()
