# Jackson: Voice-controlled Jacket
# Microphone capture logic.
# Author: Tony DiCola
# License: MIT https://opensource.org/licenses/MIT
import alsaaudio

import config


class Microphone:

    def __init__(self):
        # Open the microphone and configure it for mono recording with signed
        # 16-bit samples.
        self._mic = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
                                  alsaaudio.PCM_NONBLOCK,
                                  device=config.DEVICE)
        self._mic.setchannels(1)
        self._mic.setrate(config.SAMPLE_RATE_HZ)
        self._mic.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self._mic.setperiodsize(512)
        # Store a copy of the last sample for use with spectrogram
        # animations.  This really should be protected behind a lock for
        # thread safe access but for speed and simplicity any hiccups in
        # the animation from contention and races here are ignored
        self.last_read = None

    def read(self):
        """Read a buffer of microphone sample data and return it.  If data
        couldn't be read then None/null is returned.
        """
        # Get a buffer of sample data from PyAlsaAudio library.
        len, buf = self._mic.read()
        # If no data was retrieved indicate it with a None value.
        if len is None:
            self.last_read = None
            return None
        # Save the sample buffer and return it.
        self.last_read = buf
        return buf
