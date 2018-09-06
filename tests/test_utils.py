import unittest

import utils


class UtilsTests(unittest.TestCase):

    def test_lerp(self):
        val = utils.lerp(0.5, 0.0, 1.0, 0.0, 10.0)
        self.assertEqual(val, 5.0)

    def test_clamp_below(self):
        val = utils.clamp(-10, 0.0, 1.0)
        self.assertEqual(val, 0.0)

    def test_clamp_above(self):
        val = utils.clamp(10, 0.0, 1.0)
        self.assertEqual(val, 1.0)

    def test_clamp_in_range(self):
        val = utils.clamp(0.5, 0.0, 1.0)
        self.assertEqual(val, 0.5)
