import sys
import inspect


def get_interface(target):
    if inspect.isclass(target):
        target = target.__init__

    args, varargs, varkw, defaultvals = inspect.getargspec(target)

    defaultvals = defaultvals or ()
    options = dict(zip(args[-len(defaultvals):], defaultvals))

    required = args
    # TODO: better to test if this is a bounded method
    if target.__name__ == '__init__':
        required = args[1:]
    if defaultvals:
        required = required[:-len(defaultvals)]

    return required, options


def run(target, argv):
    get_interface(target)


def main(func):
    module = inspect.getmodule(inspect.stack()[1][0])
    if module is None or \
            module.__name__ == '<module>' or \
            module.__name__ == '__main__':
        run(func, sys.argv)
    return func # for use as decorator
