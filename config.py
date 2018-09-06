# Jackson: Voice-controlled Jacket
# Global configuration values.
# Author: Tony DiCola
# License: MIT https://opensource.org/licenses/MIT


# Microphone config:
DEVICE             = 'plughw:1,0'   # ALSA device to use for mic input.  Be sure
                                    # to use the 'plughw' devices if your
                                    # hardware doesn't natively support the
                                    # sample rate below (most USB audio
                                    # adapters don't see to support 16khz).
SAMPLE_RATE_HZ     = 16000          # Sample rate for the mic (16khz preferred)

# NeoPixel LED configuration:
import _rpi_ws281x as ws
LED_COUNT          = 26      # Number of LED pixels.
LED_PIN            = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ        = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA            = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS     = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT         = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL        = 0       # Set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_TYPE           = ws.WS2811_STRIP_GRB  # Strip type, see rpi_ws281x library.

# Animation configuration:
FLOW_HUE_PERIOD_S  = 45.0  # Idle flow animation complete hue cycle period (sec)
ANIMATION_DURATION = 10.0  # Number of seconds animations like wink will play.

# Pocketphinx speech recognition config:
ACOUSTIC_MODEL     = '/usr/local/share/pocketsphinx/model/en-us/en-us'
DICTIONARY_MODEL   = '/usr/local/share/pocketsphinx/model/en-us/cmudict-en-us.dict'
LANGUAGE_MODEL     = '/usr/local/share/pocketsphinx/model/en-us/en-us.lm.bin'
POCKETSPHINX_DEBUG = True # Bool to enable/disable pocketsphinx debug output.

# Speech command configuration:
GRAMMAR_MODEL      = './commands.gram'  # JSGF grammar for Pocketsphinx
COMMAND_MIN_S      = 2.0  # Min time to wait for a command to start (seconds).
COMMAND_MAX_S      = 5.0  # Max time to record voice for a command (seconds).
# Junk words that will be ignored by command processing.  This MUST match the
# grammar <junk> rule list!
GRAMMAR_JUNK       = set(['please', 'thank you', 'thanks', 'the', 'your', 'to'])

# Keyword configuration.
# These are wake, happy, and sad keywords that will be continuously detected
# by Pocketsphinx.  Each dict is a mapping of keyword utterance to its
# associated threshold.  See the Pocketsphinx project for details on the
# threshold value, but in general it can be tuned up or down (from 1e-05 to
# 1e-20 for example) to tweak the accuracy of keyword recognition.
WAKE_WORDS = {
    'yo jackson': '1e-05'
}
HAPPY_WORDS = {
    'happiness':  '1e-05',
    'respect':    '1e-05',
    'excitement': '1e-05'
}
SAD_WORDS = {
    'sadness':    '1e-05',
    'depression': '1e-05',
    'anger':      '1e-05'
}

# Mapping of color hue strings/names to their value (in degrees).
COLOR_HUES = {
    'red':         0.0,
    'orange':     30.0,
    'yellow':     60.0,
    'green':     120.0,
    'turquoise': 150.0,
    'cyan':      180.0,
    'blue':      210.0,
    'violet':    240.0,
    'purple':    270.0,
    'magenta':   300.0,
    'scarlet':   330.0
}

# Mapping of brightness strings to their value (0...3, off to full bright).
BRIGHTNESS_VALUES = {
    'zero':   0,
    'one':    1,
    'two':    2,
    'three':  3,
    'low':    1,
    'medium': 2,
    'high':   3,
    'max':    3
}
