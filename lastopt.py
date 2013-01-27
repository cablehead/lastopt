import re
import sys
import inspect

from optparse import OptionParser
from optparse import make_option


def to_OptionParser(options):
    # add options, automatically detecting their -short and --long names

    single_char_prefix_re = re.compile('^[a-zA-Z0-9]_')

    optypes=[int, long, float, complex] # not type='choice' choices='a|b'
    def optype(t):
        if t is bool:
            return None
        if t in optypes:
            return t
        return "string"

    # TODO:
    # helpdict = getattr(func, 'optfunc_arghelp', {})
    helpdict = {}

    opt = OptionParser()

    shortnames = set(['h'])
    for name in options.iterkeys():
        if single_char_prefix_re.match(name):
            shortnames.add(name[0])

    for original, default in options.iteritems():
        name = original
        # x_argument forces short name for argument to be x
        if single_char_prefix_re.match(name):
            short = name[0]
            name = name[2:]
            opt._custom_names[name] = original

        # or we pick the first letter from the name not already in use:
        else:
            short=None
            for s in name:
                if s not in shortnames:
                    short=s
                    break
        names = []
        if short is not None:
            shortnames.add(short)
            short_name = '-%s' % short
            names.append(short_name)

        clean_name = name.replace('_', '-')
        long_name = '--%s' % clean_name
        names.append(long_name)

        if isinstance(default, bool):
            no_name='--no%s' % clean_name
            opt.add_option(make_option(
                no_name,
                action='store_false',
                dest=name,
                help = helpdict.get(original, 'unset %s' % long_name)))
            action = 'store_true'

        else:
            action = 'store'

        example = str(default)
        if isinstance(default, int):
            if default==sys.maxint: example = "INFINITY"
            if default==(-sys.maxint-1): example = "-INFINITY"

        help_post = ' (default: %s)' % example

        opt.add_option(make_option(*names,
            action=action,
            dest=name,
            default=default,
            help=helpdict.get(original, '') + help_post,
            type=optype(type(default))))

    return opt


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
    ret = ''
    if target.__doc__:
        ret += target.__doc__ + '\n'
    ret += "usage: %s %s%s" % (
        argv[0],
        ' '.join('<%s>' % a for a in required),
        optional and ' [options]' or '')
    return ret


def parse(argv, target):
    required, optional = get_interface(target)
    args = argv[1:]
    if len(args) < len(required):
        print usage(argv, target)
        sys.exit(1)
    a = args[:len(required)]

    args = args[len(required):]
    if optional:
        parser = to_OptionParser(optional)
        opt, remaining = parser.parse_args(args)
        # TODO: create ability to chain sub-commands
        # TODO: should show full usage
        if remaining:
            print usage(argv, target)
            sys.exit(1)
        kw = opt.__dict__

    return a, kw


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
