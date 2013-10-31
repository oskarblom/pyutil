from datetime import date
import json
import pprint

def dictify(current):
    """ Convert object graph to dict. Can't handle cyclic refs. """

    if hasattr(current, "__dict__"):
        return dictify(vars(current))

    elif isinstance(current, dict):
        for key, val in current.iteritems():
            current[dictify(key)] = dictify(val)
        return current

    elif hasattr(current, "__iter__"):
        return map(dictify, current)

    elif isinstance(current, date):
        return str(current)

    else:
        return current

def filedump(content, filename, append=True):
    with open(filename, "a" if append else "w") as f:
        f.write(content)

def dump(o):
    return pprint.pformat(dictify(o), indent=2)

def jsondump(o):
    return json.dumps(dictify(o), indent=4)

def filedump_obj(o, filename, append=True):
    filedump(dump(o), filename, append)

def filedump_jsonobj(o, filename, append=True):
    filedump(jsondump(o), filename, append)

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

    print dump(f)
    print dump({"foo": f})
    print dump([1, 2, f])
    print dump("foobar")
    print dump(123)
