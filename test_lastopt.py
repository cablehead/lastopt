import unittest

import lastopt


class InterfaceTest(unittest.TestCase):
    def test_basic(self):
        def f(a, b, c=1, d='foo'):
            pass
        got = lastopt.get_interface(f)
        self.assertEqual(got, (['a', 'b'], {'c': 1, 'd': 'foo'}))

        class F(object):
            def __init__(self, a, b, c=1, d='foo'):
                pass
        got = lastopt.get_interface(F)
        self.assertEqual(got, (['a', 'b'], {'c': 1, 'd': 'foo'}))

    def test_to_OptionParser(self):
        parser = lastopt.to_OptionParser({'foo': 'bar'})
        argv = ['-f', 'ted']
        options, a = parser.parse_args(argv)
        self.assertEqual(options.foo, 'ted')

        parser = lastopt.to_OptionParser({'num': 3})
        argv = ['--num=5']
        options, a = parser.parse_args(argv)
        self.assertEqual(options.num, 5)

        parser = lastopt.to_OptionParser({'toggle': False})
        argv = []
        options, a = parser.parse_args(argv)
        self.assertEqual(options.toggle, False)
        argv = ['-t']
        options, a = parser.parse_args(argv)
        self.assertEqual(options.toggle, True)
        argv = ['--toggle']
        options, a = parser.parse_args(argv)
        self.assertEqual(options.toggle, True)

        parser = lastopt.to_OptionParser({'to_email': 'bar'})
        argv = ['--to-email', 'ted']
        options, a = parser.parse_args(argv)
        self.assertEqual(options.to_email, 'ted')

    def test_select_command_from_list_of_functions(self):
        def m_1(a):
            return a
        def m_2(b=2):
            return b
        self.assertEqual(lastopt.run(['m-1', 3], [m_1, m_2]), 3)
        self.assertEqual(lastopt.run(['m-2'], [m_1, m_2]), 2)

    def test_select_command_from_class(self):
        class C(object):
            def m_1(self, a):
                return a
            def m_2(self, b=2):
                return b
        c = C()
        self.assertEqual(lastopt.run(['m-1', 3], c), 3)
        self.assertEqual(lastopt.run(['m-2'], c), 2)

    def test_select_command_from_list_of_classes(self):
        class User(object):
            def __init__(self, user_id):
                self.user_id = user_id
            def name(self):
                return "name for user: %s" % self.user_id

        class Room(object):
            def __init__(self, room_id):
                self.room_id = room_id
            def members(self):
                return "members for room: %s" % self.room_id

        self.assertEqual(
            lastopt.run(['user', 123, 'name'], [User, Room]),
            'name for user: 123')
