
"""
bork env staging start msginabox -i c1.medium

bork env staging.re run 

bork install msginabox
"""

import lastopt

@lastopt.main
def hello(world='world'):
    print 'hello %s' % world
