lastopt
=======

lastopt is a Python utility for quickly creating command line utilities using
function and class introspection.

lastopt is licensed under the Apache Licence, Version 2.0
(http://www.apache.org/licenses/LICENSE-2.0.html).

Example
-------

```python
#!/usr/bin/env python


import lastopt


def install(package, dependencies=False):
    print "install %s, with dependencies: %s" % (
        package, dependencies and 'yes' or 'no')


class Env(object):
    def __init__(self, name):
        self.name = name

    def start(self, package):
        print "starting %s.%s" % (self.name, package)


lastopt.main([install, Env])
```

$ ./command

    Usage: ./command COMMAND [ARGS]

    The available commands are:
        env
        install

$ ./command install --help

    Usage: ./command install <package> [options]

    Options:
      -h, --help          show this help message and exit
      --nodependencies    unset --dependencies
      -d, --dependencies   (default: False)

$ ./command install redis -d

    install redis, with dependencies: yes

$ ./command env production

    Usage: ./command env production COMMAND [ARGS]

    The available commands are:
        start

$ ./command env production start frontend

    starting production.frontend

History
-------

lastopt is directly inspired by Simon Willson's clever introspection hack from
a few years back: https://github.com/simonw/optfunc
