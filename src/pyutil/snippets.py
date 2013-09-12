from datetime import date
from pprint import pprint

def dictify(current):
    """ Convert object graph to dict. Can't handle cyclic refs. """

    if hasattr(current, "__dict__"):
        struct = {}
        for attr in vars(current):
            struct[attr] = dictify(getattr(current, attr))
        return struct

    elif isinstance(current, dict):
        for key, val in current.iteritems():
            current[key] = dictify(val)
        return current

    elif hasattr(current, "__iter__"):
        return map(dictify, current)

    elif isinstance(current, date):
        return str(current)

    else:
        return current

def dump(o):
    pprint(dictify(o), indent=2)

if __name__ == "__main__":

    class Foo(object):
        pass

    class Bar(object):
        pass

    b = Bar()
    b.a = "b"
    b.c = 2

    f = Foo()
    f.a = [b]
    f.b = 23.14
    f.z = { "fizz": b }

    dump(f)
    dump({"foo": f})
    dump([1, 2, f])
    dump("foobar")
    dump(123)
