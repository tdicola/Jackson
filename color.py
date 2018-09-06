# Jackson: Voice-controlled Jacket
# Color utility functions.
# Author: Tony DiCola
# License: MIT https://opensource.org/licenses/MIT
import math

import utils


# Build a simple gamma correction table for more accurate color lookups.
gamma8 = bytearray(256)
for i in range(len(gamma8)):
    gamma8[i] = int(math.pow(i/255.0, 2.8)*255.0+0.5) & 0xFF

def compose(red, green, blue):
    """Generate a 24-bit RGB color value from the provided red, green, blue
    component byte values.
    """
    return (((red & 0xFF) << 16) | ((green & 0xFF) << 8) | (blue & 0xFF)) & 0xFFFFFF

def decompose(color):
    """Retrieve the red, green, blue component byte values from a 24-bit RGB
    color value.  Returns a 3-tuple of byte values (red, green, blue).
    """
    return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

def lerp(x, x0, x1, c0, c1):
    """Linear interpolation of 24-bit color values.  Given a value x within
    the range x0, x1 and colors c0, c1 this will return a color c that is
    linearly interpolated within c0, c1 proportional to x within x0, x1.
    """
    r0, g0, b0 = decompose(c0)
    r1, g1, b1 = decompose(c1)
    return compose(utils.clamp(int(utils.lerp(x, x0, x1, r0, r1)), 0, 255),
                   utils.clamp(int(utils.lerp(x, x0, x1, g0, g1)), 0, 255),
                   utils.clamp(int(utils.lerp(x, x0, x1, b0, b1)), 0, 255))

def hsv_to_rgb(h, s, v):
    """Convert a hue, saturation, value color into a 24-bit gamma correct
    RGB color.  Hue should be a value in degrees from 0-360, and saturation &
    value should be a floating point value from 0 to 1 (max intensity).
    """
    # Convert HSV color to RGB color.  Input is:
    #  h = hue, from 0 to 360 degrees
    #  s = saturation, from 0 to 1.0
    #  v = value, from 0 to 1.0
    # The returned color will be a 24-bit value that is gamma corrected.
    # Adapted from: https://www.cs.rit.edu/~ncs/color/t_convert.html
    if s == 0:
        return compose(int(v * 255), int(v * 255), int(v * 255))
    h /= 60.0
    i = math.floor(h)
    f = h - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    r, g, b = 0, 0, 0
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    return compose(gamma8[int(r * 255)], gamma8[int(g * 255)],
                   gamma8[int(b * 255)])
