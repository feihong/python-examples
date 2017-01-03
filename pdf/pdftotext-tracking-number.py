"""
Grab the tracking numbers content from a document that contains a mix of
domestic and foreign labels.

Note that if we just grab the text from the entire page, the text will be out of order because the labels are sideways.

"""
import os
import sys
import subprocess
import re
from PyPDF2 import PdfFileReader


path = os.environ['PRIVATE_DATA'] + '/ebay/12-labels.pdf'


TOP_BBOX = 140, 95, 30, 195
BOTTOM_BBOX = 140, 495, 30, 195
FOREIGN_BBOX = 265, 275, 250, 100


def main():
    for page in range(1, 8):
        out = '{}: {}'.format(page, get_tracking_numbers(page))
        print(out)


def get_tracking_numbers(page):
    result = []

    for bbox in (TOP_BBOX, BOTTOM_BBOX):
        text = get_tracking_number(page, bbox)
        if re.match(r'\d{22}', text):
            result.append(text)

    text = get_tracking_number(page, FOREIGN_BBOX)
    if re.match(r'[A-Z]{2}\d{9}US', text):
        result.append(text)

    return result


def get_tracking_number(page, bbox):
    result = get_text_for_bbox(page, *bbox)
    return result.strip().replace(' ', '')


def get_text_for_bbox(page, x, y, w, h):
    page = str(page)
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
