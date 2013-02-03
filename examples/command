import lastopt


class Env(object):
    def __init__(self, name):
        self.name = name

    def start(self, package):
        print "starting %s.%s" % (self.name, package)


def install(package):
    print "install %s" % (package,)


lastopt.main([Env, install])
