import unittest

import color


class ColorTests(unittest.TestCase):

    def test_decompose(self):
        red, green, blue = color.decompose(0x010203)
        self.assertEqual(red, 1)
        self.assertEqual(green, 2)
        self.assertEqual(blue, 3)

    def test_compose(self):
        val = color.compose(1, 2, 3)
        self.assertEqual(val, 0x010203)

    def test_lerp(self):
        val = color.lerp(0.5, 0.0, 1.0, 0x000000, 0xFFFFFF)
        self.assertEqual(val, 0x7F7F7F)

    def test_hsv_to_rgb(self):
        val = color.hsv_to_rgb(0.0, 1.0, 1.0)
        self.assertEqual(val, 0xFF0000)

    def test_hsv_to_rgb_zero_value(self):
        val = color.hsv_to_rgb(0.0, 1.0, 0.0)
        self.assertEqual(val, 0)
