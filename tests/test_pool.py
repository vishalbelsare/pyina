#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

from dill import source, temp
def run_source(obj):
    _obj = source._wrap(obj)
    assert _obj(1.57) == obj(1.57)
    src = source.importable(obj, alias='_f')
    exec src in globals(), locals()
    assert _f(1.57) == obj(1.57)
    name = source.getname(obj)
    assert name == obj.__name__ or src.split("=",1)[0].strip()

def run_files(obj):
    f = temp.dump_source(obj, alias='_obj')
    _obj = temp.load_source(f)
    assert _obj(1.57) == obj(1.57)

def run_pool(obj):
    from pyina.launchers import Mpi
    p = Mpi(2)
    x = [1,2,3]
    y = map(obj, x)
    p.scatter = False
    assert p.map(obj, x) == y
    p.source = True
    assert p.map(obj, x) == y
    p.scatter = True
    assert p.map(obj, x) == y
    p.source = False
    assert p.map(obj, x) == y


def test_pyina():
    from math import sin
    f = lambda x:x+1
    def g(x):
        return x+2

    for func in [g, f, abs, sin]:
        run_source(func)
        run_files(func)
        run_pool(func)


if __name__ == '__main__':
    test_pyina()
