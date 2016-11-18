"""
List all Chinese fonts.

"""
import subprocess

cmd = 'fc-list -f "%{family}\n" :lang=zh'
output = subprocess.check_output(cmd, shell=True).decode('utf-8')

names = set()

for line in output.splitlines():
    if ',' in line:
        # import pdb; pdb.set_trace()
        for name in line.split(','):
            names.add(name)
    else:
        names.add(line)

names = list(names)
names.sort()
for name in names:
    print(name)
