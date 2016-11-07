import itertools
import time
import sys


start = int(sys.argv[1])

try:
    for i in itertools.count(start):
        print('Hello {}'.format(i))
        time.sleep(1)
except KeyboardInterrupt:
    print('Quitting...')
    time.sleep(2)
    print('Done!')
