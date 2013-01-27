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
