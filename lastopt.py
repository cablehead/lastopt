import sys
import inspect


def get_interface(target):
    if inspect.isclass(target):
        target = target.__init__

    args, varargs, varkw, defaultvals = inspect.getargspec(target)

    defaultvals = defaultvals or ()
    optional = dict(zip(args[-len(defaultvals):], defaultvals))

    required = args
    # TODO: better to test if this is a bounded method
    if target.__name__ == '__init__':
        required = args[1:]
    if defaultvals:
        required = required[:-len(defaultvals)]

    return required, optional


def usage(argv, target):
    required, optional = get_interface(target)
    return "usage: %s %s%s" % (
        argv[0],
        ' '.join('<%s>' % a for a in required),
        optional and ' [options]' or '')


def parse(argv, target):
    required, optional = get_interface(target)
    args = argv[1:]
    if len(args) < len(required):
        print usage(argv, target)
        sys.exit(1)
    a = args[:len(required)]
    return a, {}


def run(argv, target):
    a, kw = parse(argv, target)
    target(*a, **kw)


def main(target):
    module = inspect.getmodule(inspect.stack()[1][0])
    if module is None or \
            module.__name__ == '<module>' or \
            module.__name__ == '__main__':
        run(sys.argv, target)
    return target # for use as decorator
