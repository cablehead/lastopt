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

    def test_select_command_from_tuple(self):
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
