#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pyina/LICENSE

__doc__ = """
# print rank - hostname info
# To run:

alias mpython='mpirun -np [#nodes] `which python`'
mpython machines_raw.py
"""

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())


if __name__ == '__main__':

    try:
        from pyina.mpi_scatter import parallel_map
        import pyina
        world = pyina.mpi.world

        hostnames = parallel_map(host, range(world.size))

        if world.rank == 0:
            print '\n'.join(hostnames)
    except:
        print __doc__
        

# end of file
