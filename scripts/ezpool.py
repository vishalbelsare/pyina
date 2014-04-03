#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE
"""
ezpool: helper script for pyina.mpi maps using the 'worker pool' strategy
(same exact code as ezscatter, but uses pyina.mpi_pool)

This is a helper script for pyina's mpi.Mapper class. Don't use it directly.
"""

import logging
log = logging.getLogger("ezpool")
log.addHandler(logging.StreamHandler())
def _debug(boolean):
    """print debug statements"""
    if boolean: log.setLevel(logging.DEBUG)
    else: log.setLevel(logging.WARN)
    return


if __name__ == '__main__':

    from pyina.mpi_pool import parallel_map
    import dill as pickle
    import sys
    import os
    from pyina import mpi
    world = mpi.world

    funcname = sys.argv[1]
    argfilename = sys.argv[2]
    outfilename = sys.argv[3]

    if funcname.endswith('.pik'):  # used pickled func
        workdir = None
        func = pickle.load(open(funcname,'r'))
    else:  # used tempfile for func
        workdir = sys.argv[4]
        sys.path = [workdir] + sys.path
        modname = os.path.splitext(os.path.basename(funcname))[0]
        module = __import__(modname)
        sys.path.pop(0)
        func = module.FUNC
    args,kwds = pickle.load(open(argfilename,'r'))

    if world.rank == 0:
        log.info('funcname: %s' % funcname)        # sys.argv[1]
        log.info('argfilename: %s' % argfilename)  # sys.argv[2] 
        log.info('outfilename: %s' % outfilename)  # sys.argv[3]
        log.info('workdir: %s' % workdir)          # sys.argv[4]
        log.info('func: %s' % func)
        log.info('args: %s' % str(args))
        log.info('kwds: %s' % str(kwds))
    res = parallel_map(func, *args, **kwds) #XXX: called on ALL nodes ?

    if world.rank == 0:
        log.info('res: %s' % str(res))
        pickle.dump(res, open(outfilename,'w'))


# end of file
