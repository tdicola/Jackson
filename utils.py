# Jackson: Voice-controlled Jacket
# Small utility functions.
# Author: Tony DiCola
# License: MIT https://opensource.org/licenses/MIT


def lerp(x, x0, x1, y0, y1):
    """Linear interpolation of a value y within y0, y1 given a value x within
    x0, x1.
    """
    return y0+(x-x0)*((y1-y0)/(x1-x0))

def clamp(x, x0, x1):
    """Clamp the value x to be within x0, x1 (inclusive)."""
    return max(min(x, x1), x0)
