import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def patch_print(filelike_obj):
    """
    Context manager that changes where the arguments of print() go to.

    """
    stdout = sys.stdout
    sys.stdout = filelike_obj
    yield
    sys.stdout = stdout


print('Before using context manager')

output = StringIO()
with patch_print(output):
    print('Cool beans')
    print('Amaze balls')
    print('Awesome sauce')

print('After using context manager')
print('\nOutput:')
print(output.getvalue())
