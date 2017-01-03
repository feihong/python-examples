"""
Grab the tracking numbers content from a page that contains two domestic labels.

Note that if we just grab the text from the entire page, the text will be out of order because the labels are sideways.

Running this script on the 7th page (containing the foreign label) won't grab
any numbers at all.

"""
import os
import sys
import subprocess
from PyPDF2 import PdfFileReader


path = os.environ['PRIVATE_DATA'] + '/ebay/12-labels.pdf'
page = sys.argv[1]


def main():
    # Top label.
    print(get_text_for_rect(140, 95, 30, 195))
    print('='*75)
    # Bottom label.
    print(get_text_for_rect(140, 495, 30, 195))


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
