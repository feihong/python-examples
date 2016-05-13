import sys
from io import StringIO


stdout = sys.stdout
output = StringIO()
print('Changing sys.stdout to StringIO object')
sys.stdout = output

print('what the dillio')
print('are you seeing this?')

sys.stdout = stdout
print('done!')
print(output.getvalue())
