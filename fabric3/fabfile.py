"""
To run the host_type task:

    fab -H localhost,some-other-host host_type

"""
from io import StringIO
from fabric.api import run
from fabric.operations import put


def host_type():
    run('uname -sa')


def upload():
    import datetime
    sio = StringIO()
    sio.write('This file was generated at %s\n\n' % datetime.datetime.now())
    put(local_path=sio, remote_path='~/cool_file.txt')
