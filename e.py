
"""
bork env staging start msginabox -i c1.medium

bork env staging.re run 

bork install msginabox
"""

import lastopt

@lastopt.main
def hello(first, second, world='world'):
    print first, second, world


# @lastopt.main
def hello(first, *a, **kw):
    print 'hello %s' % (first,)
