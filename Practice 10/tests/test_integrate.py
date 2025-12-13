import unittest
import math
from functions.integrate import integrate


class TestIntegrate(unittest.TestCase):
    def test_cos_integral(self):
        result = integrate(math.cos, 0, math.pi / 2, n_iter=100000)
        self.assertAlmostEqual(result, 1.0, delta=1e-4)

    def test_sin_integral(self):
        result = integrate(math.sin, 0, math.pi, n_iter=100000)
        self.assertAlmostEqual(result, 2.0, delta=1e-4)

    def test_polynomial(self):
        result = integrate(lambda x: x ** 2 + 2 * x + 1, 0, 3, n_iter=100000)
        self.assertAlmostEqual(result, 21.0, delta=1e-4)

    def test_stability(self):
        r1 = integrate(lambda x: x, 0, 1, n_iter=1000)
        r2 = integrate(lambda x: x, 0, 1, n_iter=100000)
        self.assertAlmostEqual(r1, 0.5, delta=1e-3)
        self.assertAlmostEqual(r2, 0.5, delta=1e-6)

    def test_invalid_bounds(self):
        with self.assertRaises(ValueError):
            integrate(math.sin, 1, 0)

    def test_invalid_iterations(self):
        with self.assertRaises(ValueError):
            integrate(math.sin, 0, math.pi, n_iter=0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
