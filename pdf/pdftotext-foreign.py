"""
Grab the tracking number from a page that contains one foreign label.

This will only work for the 7th page (the only one containing a foreign label).

"""
import os
import sys
import subprocess
from PyPDF2 import PdfFileReader


path = os.environ['PRIVATE_DATA'] + '/ebay/12-labels.pdf'
page = sys.argv[1]


def main():
    print(get_text_for_rect(265, 275, 250, 100))


def get_text_for_rect(x, y, w, h):
    cmd = [
        'pdftotext',
        str(path),
        '-f', page,    # first page
        '-l', page,    # last page
        '-x', str(x),
        '-y', str(y),
        '-W', str(w),
        '-H', str(h),
        '-'
    ]
    return subprocess.check_output(cmd).decode('utf-8')


if __name__ == '__main__':
    main()
