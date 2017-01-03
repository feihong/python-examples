"""
Grab the tracking numbers content from a page that contains two domestic labels.

Note that if we just grab the text from the entire page, the text will be out of order because the labels are sideways.

Running this script on the 7th page (containing the foreign label) won't grab
any numbers at all.

"""
import os
import sys
import subprocess
import re
from PyPDF2 import PdfFileReader


path = os.environ['PRIVATE_DATA'] + '/ebay/12-labels.pdf'
page = sys.argv[1]

TOP_BBOX = 140, 95, 30, 195
BOTTOM_BBOX = 140, 495, 30, 195


def main():
    for tn in get_tracking_numbers():
        print(tn)


def get_tracking_numbers():
    result = []
    for bbox in (TOP_BBOX, BOTTOM_BBOX):
        text = get_tracking_number(bbox)
        if re.match(r'\d{22}', text):
            result.append(text)
    return result



def get_tracking_number(bbox):
    result = get_text_for_bbox(*bbox)
    return result.strip().replace(' ', '')


def get_text_for_bbox(x, y, w, h):
    cmd = [
        'pdftotext',
        str(path),
        '-f', page,    # first page
        '-l', page,    # last page
        # Crop parameters
        '-x', str(x),
        '-y', str(y),
        '-W', str(w),
        '-H', str(h),
        # Send output to stdout
        '-'
    ]
    return subprocess.check_output(cmd).decode('utf-8')


if __name__ == '__main__':
    main()
