# Jackson: Voice-controlled Jacket
# Main logic.
# Author: Tony DiCola
# License: MIT https://opensource.org/licenses/MIT
import logging
import math
import numbers
import random
import time
import threading

import numpy as np

import color
import commands
import config
import lights
import microphone
import speech
import utils


# TODO:
# - Add command threshold (i.e. score above 3000 or so)
# - Add color.py tests
# - Bug: stop iteration when not in idle will force back into idle (say happy during other animation) - It's time to add a proper animation stack
# - Put generic animation functions (between, duration, etc.) in animations.py
# - Make wink go 'off (half)' - 'on' for 0.75 seconds


logger = logging.getLogger(__name__)


class Jackson:

    def __init__(self):
        self._microphone = microphone.Microphone()
        self._speech = speech.SpeechRecognizer(self._microphone)
        self._lights = lights.Lights()
        self._keywords = commands.Dispatcher()
        self._commands = commands.Dispatcher(junk=config.GRAMMAR_JUNK)
        self._happiness = 0  # Value that goes from -3 to 3
        self._brightness = 2 # Value that goes from 0 to 3
        self._hue = 0.0
        self._animation = self._idle_animation()
        self._state_lock = threading.RLock()
        self._animation_lock = threading.RLock()
        # Configure the keywords and their associated callbacks.
        for w in config.WAKE_WORDS:
            self._keywords.register(w, self._wake)
        for w in config.HAPPY_WORDS:
            self._keywords.register(w, self._increment_happiness, 1)
        for w in config.SAD_WORDS:
            self._keywords.register(w, self._increment_happiness, -1)
        # Configure the command parsing based on Jackson's grammar (from
        # commands.gram).  Right now this is all manual configuration and
        # care must be taken to ensure the logic below and commands.gram
        # are kept up to date.
        self._commands.register('wink', self._wink)
        self._commands.register('spectrum', self._spectrum)
        self._commands.register('sparkle', self._sparkle)
        self._commands.register('knight rider', self._knight_rider)
        self._commands.register('brighter', self._increment_brightness, 1)
        self._commands.register('dimmer', self._increment_brightness, -1)
        self._commands.register_starts_with('show me', self._change_animation)
        self._commands.register_starts_with('light up', self._change_color)
        self._commands.register_starts_with('change', self._change)
        self._commands.register_starts_with('set', self._change)
        self._commands.register_starts_with('update', self._change)
        self._commands.register_starts_with('modify', self._change)
        self._commands.register_starts_with('make', self._change)

    def _animate(self, animation):
        with self._animation_lock:
            self._animation = animation

    # Properties that define Jackon's state:
    @property
    def happiness(self):
        with self._state_lock:
            return self._happiness

    @happiness.setter
    def happiness(self, val):
        with self._state_lock:
            if val is None:
                self._happiness = 0
            else:
                self._happiness = utils.clamp(int(val), -3, 3)
            logger.debug('Happiness: {0}'.format(self._happiness))

    @property
    def happiness_freq(self):
        # Convert happiness into an animation speed/frequency.
        return utils.lerp(self.happiness, -3.0, 3.0, 1.0/4.0, 2.0)

    @property
    def brightness(self):
        with self._state_lock:
            return self._brightness

    @brightness.setter
    def brightness(self, val):
        with self._state_lock:
            if val is None:
                self._brightness = 0
            elif isinstance(val, numbers.Number):
                self._brightness = utils.clamp(int(val), 0, 3)
            else:
                self._brightness = config.BRIGHTNESS_VALUES.get(val, self._brightness)
            logger.debug('Brightness: {0}'.format(self._brightness))

    @property
    def brightness_hsv(self):
        return utils.lerp(self.brightness, 0.0, 3.0, 0.0, 1.0)

    @property
    def hue(self):
        with self._state_lock:
            return self._hue

    @hue.setter
    def hue(self, val):
        with self._state_lock:
            if val is None:
                self._hue = 0
            elif isinstance(val, numbers.Number):
                self._hue = math.fmod(val, 360.0)
            else:
                self._hue = config.COLOR_HUES.get(val, self._hue)

    # Keyword callbacks:
    def _wake(self, command):
        # Green/yellow pulse while listening.
        pulse = self._create_pulse_animation(80.0, 2.0)
        self._animate(pulse)
        command, score = self._speech.listen_command()
        self._animate(self._animate_between(0.0, 1.0, pulse, self._idle_animation()))
        logger.debug('Detected keyword: {0} [score: {1}]'.format(command, score))
        # TODO: Add score threshold?
        self._commands.dispatch(command)

    def _increment_happiness(self, command, val):
        self.happiness += val
        if val > 0:
            old = self._animation
            self._animate(self._animate_between(0.5, 1.5,
                self._create_pulse_animation(350.0, 1.0),
                old))
        else:
            old = self._animation
            self._animate(self._animate_between(0.5, 1.5,
                self._create_pulse_animation(240.0, 1.0),
                old))

    # Command callbacks:
    def _wink(self, command):
        logger.debug('Wink animation')
        self._animate(self._animate_duration(0.75, self._wink_animation))

    def _spectrum(self, command):
        logger.debug('Spectrum animation')
        self._animate(self._animate_between(config.ANIMATION_DURATION, 1.0,
            self._spectrum_animation(), self._idle_animation()))

    def _sparkle(self, command):
        logger.debug('Sparkle animation')
        self._animate(self._animate_between(config.ANIMATION_DURATION, 1.0,
            self._sparkle_animation(), self._idle_animation()))

    def _knight_rider(self, command):
        logger.debug('Knight Rider animation')
        self._animate(self._animate_between(config.ANIMATION_DURATION, 1.0,
            self._knight_rider_animation(), self._idle_animation()))

    def _increment_brightness(self, command, val):
        self.brightness += val

    def _change(self, command):
        logger.debug('Change command: {0}'.format(command))
        if len(command) < 2:
            return
        state = command[1]
        if state == 'color':
            self._change_color(command)
        elif state == 'brightness':
            self.brightness = command[2]

    def _change_color(self, command):
        logger.debug('Change color')
        if len(command) < 3:
            return
        self.hue = command[2]
        # Snap straight to animating at this new hue and stop any fade out.
        self._animate(self._idle_animation())

    def _change_animation(self, command):
        logger.debug('Change animation')
        if len(command) < 3:
            return
        self._commands.dispatch(' '.join(command[2:]))

    # Basic animation functions.  These are generator functions that yield a
    # pixel color every time they are called.
    def _idle_animation(self):
        n = len(self._lights)
        while True:
            t = time.time()
            max_val = self.brightness_hsv
            min_val = 0.5 * max_val
            for i in range(n):
                phase = i/(n-1)*2.0*math.pi
                x = math.sin(2.0*math.pi*self.happiness_freq*t + phase)
                value = utils.lerp(x, -1.0, 1.0, max_val, min_val)
                yield color.hsv_to_rgb(self.hue, 1.0, value)

    def _sparkle_animation(self):
        n = len(self._lights)
        phases = [random.uniform(0, 2.0*math.pi) for _ in range(n)]
        #frequencies = [random.uniform(0.25, 1.5) for _ in range(n)]
        f = self.happiness_freq
        frequencies = [random.uniform(f/2.0, 2.0*f) for _ in range(n)]
        while True:
            t = time.time()
            for i in range(n):
                x = math.sin(2.0*math.pi*frequencies[i]*t + phases[i])
                hue = utils.lerp(x, -1.0, 1.0, 0.0, 360.0)
                x = math.sin(2.0*math.pi*frequencies[-(i+1)]*t + phases[-(i+1)])
                value = utils.lerp(x, -1.0, 1.0, 0, self.brightness_hsv)
                yield color.hsv_to_rgb(hue, 1.0, value)

    def _knight_rider_animation(self):
        n = len(self._lights)
        while True:
            t = time.time()
            f = self.happiness_freq
            x0 = math.sin(2.0*math.pi*f*t)
            x1 = math.sin(2.0*math.pi*f*t - math.pi*(1/n))
            i0 = int(utils.lerp(x0, -1.0, 1.0, 0, n))
            i1 = int(utils.lerp(x1, -1.0, 1.0, 0, n))
            for i in range(n):
                if i == i0:
                    yield color.hsv_to_rgb(self.hue, 1.0, self.brightness_hsv)
                elif i == i1:
                    yield color.hsv_to_rgb(self.hue, 1.0, self.brightness_hsv/2)
                else:
                    yield 0

    def _spectrum_animation(self):
        n = len(self._lights)
        while True:
            # Run a FFT on the incoming audio to break it into frequency
            # buckets. Interpolate those as the intensity of hues across the
            # pixels.
            audio = self._microphone.last_read
            if audio is None or len(audio) < 4*n:
                continue
            audio = np.frombuffer(audio[:4*n], dtype='int16')
            freqs = 10*np.log10(np.abs(np.fft.rfft(audio)))
            if len(freqs) < (n+1):
                continue
            max_power = 30.0  #TODO: tune this value?
            max_value = self.brightness_hsv
            for i in range(n):
                hue = utils.lerp(i, 0, n, 0.0, 360.0)
                value = utils.lerp(freqs[i+1], 0, max_power, 0, max_value)
                value = utils.clamp(value, 0, max_value)
                yield color.hsv_to_rgb(hue, 1.0, value)

    def _wink_animation(self):
        left_on = random.random() >= 0.5
        pulse = self._create_pulse_animation(80.0, 2.0)()
        n = len(self._lights)
        half = n // 2
        while True:
            t = time.time()
            for i in range(n):
                color = next(pulse)
                if left_on and i < half:
                    yield color
                elif not left_on and i >= half:
                    yield color
                else:
                    yield 0

    # Animation creators.  These functions create animation generators that
    # are customized with special behavior or functionality.
    def _animate_duration(self, duration_s, animation):
        end = time.time() + duration_s
        #animation = animation()
        def _animate_duration_inner():
            while time.time() < end:
                yield next(animation)
            raise StopIteration
        return _animate_duration_inner()

    def _animate_between(self, first_duration, fade_duration, first, second):
        start = time.time()
        fade_start = start + first_duration
        end = fade_start + fade_duration
        n = len(self._lights)
        #first = first()
        #second = second()
        def _animate_between_inner():
            t = time.time()
            while t < fade_start:
                for i in range(n):
                    yield next(first)
                t = time.time()
            while t < end:
                for i in range(n):
                    yield color.lerp(t, fade_start, end, next(first), next(second))
                t = time.time()
            raise StopIteration
        return _animate_between_inner()

    def _create_pulse_animation(self, hue, freq_hz):
        def _pulse_animation():
            while True:
                n = len(self._lights)
                t = time.time()
                x = math.sin(2.0*math.pi*freq_hz*t)
                max_val = self.brightness_hsv
                min_val = 0.75 * max_val
                value = utils.lerp(x, -1.0, 1.0, max_val, min_val)
                for i in range(n):
                    yield color.hsv_to_rgb(hue, 1.0, value)
        return _pulse_animation()

    # Background thread to process speech keywords and commands.
    def _listen_speech(self):
        while True:
            keyword = self._speech.listen_keyword()
            self._keywords.dispatch(keyword)

    def _animate_lights(self):
        period = 1/60.0
        n = len(self._lights)
        while True:
            try:
                with self._animation_lock:
                    for i in range(n):
                        self._lights.set_pixel(i, next(self._animation))
                self._lights.show()
                time.sleep(period)
            except StopIteration:
                # Switch back to idle animation after a previous
                # animation finishes.
                self._animate(self._idle_animation())

    def _cycle_hue(self):
        period = 1/60.0
        last = time.time()
        hue_velocity = 360.0 / config.FLOW_HUE_PERIOD_S
        while True:
            # Increment the hue based on the current speed.
            now = time.time()
            delta = now - last
            last = now
            self.hue += hue_velocity*delta
            time.sleep(period)

    def main(self):
        logging.basicConfig(level=logging.DEBUG)
        self._listen_thread = threading.Thread(target=self._listen_speech)
        self._listen_thread.daemon = True
        self._listen_thread.start()
        self._animate_thread = threading.Thread(target=self._animate_lights)
        self._animate_thread.daemon = True
        self._animate_thread.start()
        self._cycle_hue()


if __name__ == '__main__':
    jackson = Jackson()
    jackson.main()
