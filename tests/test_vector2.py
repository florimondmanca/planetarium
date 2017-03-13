import unittest
import math
from tests.utils import randvec, randscalar, repeat
from src.core.utils import Vector2


def vector_amplitude(vec):
    return math.sqrt(vec.x ** 2 + vec.y ** 2)


def non_vector():
    return randscalar(), 'hello', True, [2, 3]


class TestVector2(unittest.TestCase):

    def test_create_zero_vector(self):
        u = Vector2()
        self.assertEqual(u.x, 0)
        self.assertEqual(u.y, 0)

    def test_create_integer_vector(self):
        u = Vector2(1, 2)
        self.assertEqual((u.x, u.y), (1, 2))

    def test_create_float_vector(self):
        u = Vector2(1.4, 34.2)
        self.assertEqual((u.x, u.y), (1.4, 34.2))

    def test_create_negative_vector(self):
        u = Vector2(-12, 23)
        self.assertEqual((u.x, u.y), (-12, 23))
        v = Vector2(0, -23.4)
        self.assertEqual((v.x, v.y), (0, -23.4))

    def test_create_from_pair(self):
        u = Vector2.from_pair((2, 3))
        self.assertEqual(u.x, 2)
        self.assertEqual(u.y, 3)
        v = Vector2.from_pair(u)
        self.assertEqual(v.x, 2)
        self.assertEqual(v.y, 3)

    def test_equality_with_other_vector(self):
        u = Vector2(-12, 23)
        v = Vector2(-12, 23)
        self.assertEqual(u, v)

    def test_equality_with_iterable(self):
        u = Vector2(-12, 23)
        self.assertEqual(u, (-12, 23))
        self.assertEqual(u, [-12, 23])

    def test_equality_with_nonvector_and_noniterable_returns_false(self):
        u = randvec()
        self.assertNotEqual(u, 'hello')
        self.assertNotEqual(u, 12)

    @repeat
    def test_negate_vector(self):
        u = randvec()
        w = -u
        self.assertEqual(w.x, -u.x)
        self.assertEqual(w.y, -u.y)

    @repeat
    def test_add_vectors(self):
        u = randvec()
        v = randvec()
        w = u + v
        self.assertEqual((w.x, w.y), (u.x + v.x, u.y + v.y))

    @repeat
    def test_add_vectors_ip(self):
        u = randvec()
        x, y = u.x, u.y
        v = randvec()
        u += v
        self.assertEqual(u.x, x + v.x)
        self.assertEqual(u.y, y + v.y)

    def test_add_vector_and_non_vector_raises_type_exception(self):
        u = randvec()
        for k in non_vector():
            with self.assertRaises(TypeError):
                u + k
            with self.assertRaises(TypeError):
                k + u

    @repeat
    def test_subtract_vectors(self):
        u = randvec()
        v = randvec()
        w = u - v
        self.assertEqual((w.x, w.y), (u.x - v.x, u.y - v.y))

    @repeat
    def test_subtract_vectors_ip(self):
        u = randvec()
        x, y = u.x, u.y
        v = randvec()
        u -= v
        self.assertEqual(u.x, x - v.x)
        self.assertEqual(u.y, y - v.y)

    def test_subtract_vector_and_non_vector_raises_type_exception(self):
        u = randvec()
        for k in non_vector():
            with self.assertRaises(TypeError):
                u - k
            with self.assertRaises(TypeError):
                k - u

    @repeat
    def test_multiply_by_scalar_left(self):
        u = randvec()
        k = randscalar()
        w = k * u
        self.assertEqual(w.x, k * u.x)
        self.assertEqual(w.y, k * u.y)

    @repeat
    def test_multiply_by_scalar_right(self):
        u = randvec()
        k = randscalar()
        w = u * k
        self.assertEqual(w.x, k * u.x)
        self.assertEqual(w.y, k * u.y)

    def test_multiply_two_vectors_raises_type_exception(self):
        u = randvec()
        v = randvec()
        with self.assertRaises(TypeError):
            u * v

    @repeat
    def test_divide_by_scalar_right(self):
        u = randvec()
        k = randscalar()
        w = u / k
        self.assertEqual(w.x, u.x / k)
        self.assertEqual(w.y, u.y / k)

    def test_divide_by_scalar_left_raises_type_exception(self):
        u = randvec()
        for k in non_vector():
            with self.assertRaises(TypeError):
                k / u

    def test_divide_two_vectors_raises_type_exception(self):
        u = randvec()
        v = randvec()
        with self.assertRaises(TypeError):
            u / v

    @repeat
    def test_amplitude_of_vector(self):
        u = Vector2()
        self.assertEqual(abs(u), 0)
        v = randvec()
        amp = vector_amplitude(v)
        self.assertEqual(abs(v), amp)

    @repeat
    def test_vector_as_bool(self):
        u = Vector2()
        self.assertFalse(u)
        v = randvec()
        self.assertTrue(v)

    @repeat
    def test_dot_product(self):
        u = randvec()
        v = randvec()
        dot = u | v
        self.assertEqual(dot, u.x * v.x + u.y * v.y)

    def test_dot_vector_and_nonvector_raises_type_exception(self):
        u = randvec()
        for k in non_vector():
            with self.assertRaises(TypeError):
                u | k
            with self.assertRaises(TypeError):
                k | u

    def test_cross_product(self):
        u = randvec()
        v = randvec()
        cross = u ^ v
        self.assertEqual(cross, u.x * v.y - u.y * v.x)

    def test_cross_vector_and_nonvector_raises_type_exception(self):
        u = randvec()
        for k in non_vector():
            with self.assertRaises(TypeError):
                u ^ k
            with self.assertRaises(TypeError):
                k ^ u

    @repeat
    def test_distance_between_vectors(self):
        u = randvec()
        v = randvec()
        d = u.dist(v)
        self.assertEqual(d, abs((u.x - v.x) ** 2 + (u.y - v.y) ** 2))

    def test_distance_vector_and_nonvector_raises_type_exception(self):
        u = randvec()
        for k in non_vector():
            with self.assertRaises(TypeError):
                u.dist(k)

    @repeat
    def test_distance_squared_between_vectors(self):
        u = randvec()
        v = randvec()
        d2 = u.dist2(v)
        self.assertEqual(d2, (u.x - v.x) ** 2 + (u.y - v.y) ** 2)

    def test_distance2_vector_and_nonvector_raises_type_exception(self):
        u = randvec()
        for k in non_vector():
            with self.assertRaises(TypeError):
                u.dist2(k)


if __name__ == '__main__':
    unittest.main()
