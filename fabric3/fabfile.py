"""
To run the host_type task:

    fab -H localhost,some-other-host host_type

"""

from fabric.api import run

def host_type():
    run('uname -sa')
