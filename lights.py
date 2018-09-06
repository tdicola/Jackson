# Jackson: Voice-controlled Jacket
# NeoPixel LED strip.
# Author: Tony DiCola
# License: MIT https://opensource.org/licenses/MIT
from neopixel import *

import config


class Lights:

    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        self._strip = Adafruit_NeoPixel(config.LED_COUNT,
                                        config.LED_PIN,
                                        freq_hz=config.LED_FREQ_HZ,
                                        dma=config.LED_DMA,
                                        invert=config.LED_INVERT,
                                        brightness=config.LED_BRIGHTNESS,
                                        channel=config.LED_CHANNEL,
                                        strip_type=config.LED_TYPE
                                        )
        self._strip.begin()
        # Clear the lights.
        self.fill(0)
        self._strip.show()

    def __len__(self):
        return config.LED_COUNT

    def fill(self, color):
        """Set the color of all lights."""
        for i in range(len(self)):
            self._strip.setPixelColor(i, color)

    def set_pixel(self, i, color):
        """Set the color of light at position i."""
        self._strip.setPixelColor(i, color)

    def show(self):
        """Push out the updated color buffer to the hardware."""
        self._strip.show()
