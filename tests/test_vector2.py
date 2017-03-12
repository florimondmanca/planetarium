import unittest

from random import random
import math
from src.utils import Vector2


def randscalar():
    # between -5 and 5
    return -5 + 10 * random()


def randvec():
    return Vector2(randscalar(), randscalar())


def vector_amplitude(vec):
    return math.sqrt(vec.x ** 2 + vec.y ** 2)


def repeat(times=10):
    def decorate(test_func):
        def new_test_func(*args, **kwargs):
            for _ in range(times):
                test_func(*args, **kwargs)
        return new_test_func
    return decorate


class TestVector2(unittest.TestCase):

    def test_create_zero_vector(self):
        v = Vector2()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)

    def test_create_integer_vector(self):
        v = Vector2(1, 2)
        self.assertEqual((v.x, v.y), (1, 2))

    def test_create_float_vector(self):
        v = Vector2(1.4, 34.2)
        self.assertEqual((v.x, v.y), (1.4, 34.2))

    def test_create_negative_vector(self):
        v = Vector2(-12, 23)
        self.assertEqual((v.x, v.y), (-12, 23))
        v = Vector2(0, -23.4)
        self.assertEqual((v.x, v.y), (0, -23.4))

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
        k = randscalar()
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
        k = randscalar()
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
        k = randscalar()
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
        k = randscalar()
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
        k = randscalar()
        with self.assertRaises(TypeError):
            u ^ k
        with self.assertRaises(TypeError):
            k ^ u


if __name__ == '__main__':
    unittest.main()
