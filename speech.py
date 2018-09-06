# Jackson: Voice-controlled Jacket
# Pocketsphinx speech recognition logic.  This class uses Pocketsphinx to
# perform both continuous keyword spotting and explicit grammar-based command
# recognition.
# Author: Tony DiCola
# License: MIT https://opensource.org/licenses/MIT
import logging
import tempfile
import time

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import config


logger = logging.getLogger(__name__)


class SpeechRecognizer:

    def __init__(self, microphone):
        """Create an instance of the speech recognizer with the specified
        microphone instance as input.
        """
        self._mic = microphone
        # Build a keyword file to pass to Pocketsphinx (the only way
        # Pocketsphinx can be configured unfortunately).
        self._kws = self._generate_keywords(config.WAKE_WORDS,
                                            config.HAPPY_WORDS,
                                            config.SAD_WORDS)
        logger.debug('Generated keyword file: {0}'.format(self._kws.name))
        # Configure Pocketsphinx recognition model.
        psconfig = Decoder.default_config()
        psconfig.set_string('-hmm', config.ACOUSTIC_MODEL)
        psconfig.set_string('-dict', config.DICTIONARY_MODEL)
        psconfig.set_float('-samprate', config.SAMPLE_RATE_HZ)
        psconfig.set_int('-nfft', 2048)  # Must bump up FFT size when using
                                         # fast sample rate (16khz or more).
        if not config.POCKETSPHINX_DEBUG:
            psconfig.set_string('-logfn', '/dev/null')  # Disable debug output.
        self._decoder = Decoder(psconfig)
        # Setup two searches for the pocketsphinx decoder, one for keywords and
        # another for the general language model.  These are used for keyword
        # spotting of wake words and continuous recognition once woken up.
        self._decoder.set_jsgf_file('command', config.GRAMMAR_MODEL)
        self._decoder.set_kws('keyword', self._kws.name)

    def _serialize_keywords(self, words):
        # Convert keywords into a string with one per line and the
        # weight/threshold value in the format expected by Pocketsphinx.
        return '\n'.join({'{0} /{1}/'.format(k, v) for k, v in words.items()})

    def _generate_keywords(self, *words):
        # Generate a keywords text file in a temporary location and return
        # the file.
        file = tempfile.NamedTemporaryFile(mode='w+', encoding='utf8')
        for w in words:
            file.write(self._serialize_keywords(w))
            file.write('\n')
        file.flush()
        return file

    def listen_command(self):
        """Listen for a command to be heard from the microphone using the
        grammar-based command search.  Will block until a command is recognized,
        or the maximum listen time elapses (specified in config.py).  Returns
        a 2-tuple of command string and score if a command is recognized, or
        None/null values if nothing was recognized and the timeout elapsed.
        """
        # Switch Pocketsphinx to grammar-based command search mode.
        self._decoder.set_search('command')
        self._decoder.start_utt()
        in_speech = False
        start = time.time()
        while True:
            # Stop if minimum listen time has elapsed and no speech is heard.
            if not in_speech and time.time() > (start + config.COMMAND_MIN_S):
                break
            # Stop if maximum listen time has elapsed.
            if time.time() > (start + config.COMMAND_MAX_S):
                break
            # Grab data from the microphone and process it with Pocketsphinx.
            buf = self._mic.read()
            if buf is None:
                continue
            self._decoder.process_raw(buf, False, False)
            in_speech = self._decoder.get_in_speech()
        # Check if Pocketsphinx detected a command and return it with the score.
        self._decoder.end_utt()
        hyp = self._decoder.hyp()
        if hyp is not None:
            return (hyp.hypstr.strip(), hyp.best_score)
        else:
            return (None, None)

    def listen_keyword(self):
        """Listen for a command to be heard from the microphone using the
        grammar-based command search.  Will block until a command is recognized
        and the resulting command string and score will be returned as a
        2-tuple.
        """
        # Switch Pocketsphinx to continuous keyword spotting search.
        self._decoder.set_search('keyword')
        self._decoder.start_utt()
        while True:
            # Grab data from the microphone and process it with Pocketsphinx.
            buf = self._mic.read()
            if buf is None:
                continue
            self._decoder.process_raw(buf, False, False)
            # If a keyword was detected return it.
            hyp = self._decoder.hyp()
            if hyp is not None:
                keyword = hyp.hypstr.strip()
                self._decoder.end_utt()
                return keyword
