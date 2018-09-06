import unittest
import unittest.mock

import commands


class CommandsDispatcherTests(unittest.TestCase):

    def test_register_single_word_dispatches_correctly(self):
        dispatcher = commands.Dispatcher()
        callback = unittest.mock.Mock()
        dispatcher.register('test', callback)
        dispatcher.dispatch('test')
        callback.assert_called_once_with(('test',))

    def test_register_multiple_words_dispatches_correctly(self):
        dispatcher = commands.Dispatcher()
        callback = unittest.mock.Mock()
        dispatcher.register('test word', callback)
        dispatcher.dispatch('test word')
        callback.assert_called_once_with(('test', 'word'))

    def test_register_starts_with_dispatches_correctly(self):
        dispatcher = commands.Dispatcher()
        callback = unittest.mock.Mock()
        dispatcher.register_starts_with('test word', callback)
        dispatcher.dispatch('test word one two')
        callback.assert_called_once_with(('test', 'word', 'one', 'two'))

    def test_non_registered_command_not_called(self):
        dispatcher = commands.Dispatcher()
        callback = unittest.mock.Mock()
        dispatcher.register('foo', callback)
        dispatcher.dispatch('test')
        callback.assert_not_called()

    def test_registered_args_and_kwargs_passed_to_callback(self):
        dispatcher = commands.Dispatcher()
        callback = unittest.mock.Mock()
        dispatcher.register('test', callback, 'bar', baz='baz')
        dispatcher.dispatch('test')
        callback.assert_called_once_with(('test',), 'bar', baz='baz')

    def test_junk_words_ignored(self):
        junk = ['the', 'your']
        dispatcher = commands.Dispatcher(junk=junk)
        callback = unittest.mock.Mock()
        dispatcher.register('test word', callback)
        dispatcher.dispatch('the test your word the')
        callback.assert_called_once_with(('test', 'word'))

    def test_junk_words_not_passed_to_callback(self):
        junk = ['the', 'your']
        dispatcher = commands.Dispatcher(junk=junk)
        callback = unittest.mock.Mock()
        dispatcher.register_starts_with('test word', callback)
        dispatcher.dispatch('the test your word the your one the two your the')
        callback.assert_called_once_with(('test', 'word', 'one', 'two'))

    def test_dispatch_none_is_ignored(self):
        dispatcher = commands.Dispatcher()
        callback = unittest.mock.Mock()
        dispatcher.register('test', callback)
        dispatcher.dispatch(None)
        callback.assert_not_called()
