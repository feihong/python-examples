"""
Print a list of fonts on Mac OS X, by looking inside common font directories.

Source: http://stackoverflow.com/questions/1113040/list-of-installed-fonts-os-x-c

"""
from pathlib import Path

FONT_DIRS = [
    '/System/Library/Fonts',
    '/Library/Fonts',
    '~/Library/Fonts',
]

paths = []

for font_dir in FONT_DIRS:
    font_dir = Path(font_dir).expanduser()
    for f in font_dir.iterdir():
        paths.append(f)

paths.sort(key=lambda x: x.name)
for path in paths:
    print(path.stem)
