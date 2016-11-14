"""
Print a list of fonts on Mac OS X, by using PyObjC. Note that this script does
not work in Python 3.

Source: http://stackoverflow.com/questions/1113040/list-of-installed-fonts-os-x-c

This seems to produce a more comprehensive list than scanning font directories.

"""
import sys

pyobjc_path = '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC/'
sys.path.append(pyobjc_path)
import Cocoa

manager = Cocoa.NSFontManager.sharedFontManager()
font_families = list(manager.availableFontFamilies())
font_families.sort()
for f in font_families:
    print(f)
