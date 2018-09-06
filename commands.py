# Jackson: Voice-controlled Jacket
# Command dispatcher that parses commands from raw speech text and invokes
# callback functions.
# Author: Tony DiCola
# License: MIT https://opensource.org/licenses/MIT
import logging


logger = logging.getLogger(__name__)


class Dispatcher:

    def __init__(self, junk=[]):
        """Create an instance of the command dispatcher.  Optionally specify
        a list of ignored/junk words which will be filtered from input
        commands.
        """
        # Store a mapping of exact and starts with command strings to
        # associated callback functions.
        self._exact_commands = {}
        self._starts_with_commands = {}
        self._junk = junk

    def register(self, command, callback, *args, **kwargs):
        """Associate the specified list/tuple of command strings with the
        provided callback.  If a command exactly matches this list (minus
        any ignored/junk words) then the provided callback is invoked with
        the entire command string and then any extra specified args and kwargs.
        """
        self._exact_commands[tuple(command.split())] = (callback, args, kwargs)

    def register_starts_with(self, command, callback, *args, **kwargs):
        """Associate the specified list/tuple of command strings with the
        provided callback.  If the start of a command matches this list (minus
        any ignored/junk words) then the provided callback is invoked with
        the entire command string and then any extra specified args and kwargs.
        """
        self._starts_with_commands[tuple(command.split())] = (callback, args, kwargs)

    def dispatch(self, command):
        """Process the specified raw speech command string and invoke any
        matching callbacks that were previously registered.  Junk words will
        be filtered out and ignored.
        """
        # Ignore empty/null command.
        if command is None:
            return
        # Remove junk words.
        for junk in self._junk:
            command = command.replace(junk, '')
        cleaned = tuple(command.strip().split())
        logger.debug('Cleaned: {0}'.format(cleaned))
        # First look for an exact command match and call its callback.
        callback, args, kwargs = self._exact_commands.get(cleaned, (None, None, None))
        # Failed to find an exact command, now look for a command that starts
        # with this command string and call its callback.
        if callback is None:
            for prefix, val in self._starts_with_commands.items():
                callback, args, kwargs = val
                if prefix == tuple(cleaned[:len(prefix)]):
                    break
        # Invoke the callback if one was found.
        if callback is not None:
            callback(cleaned, *args, **kwargs)
