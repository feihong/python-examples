"""
Grab the textual content from a two-label page. Note that if we just grab the
text from the entire page, the text will be out of order because the labels
are sideways.

"""
import os
import sys
import subprocess
from PyPDF2 import PdfFileReader

# Probably will not be able to extract text from this document.
path = os.environ['PRIVATE_DATA'] + '/ebay/12-labels.pdf'

page = sys.argv[1]

def main():
    # Top label.
    print(get_text_for_rect(90, 45, 460, 300))
    print('='*75)
    # Bottom label.
    print(get_text_for_rect(90, 445, 460, 300))


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
