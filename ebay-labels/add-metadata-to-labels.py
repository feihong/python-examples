"""
Domestic labels have about 3 lines, 39 characters wide worth of space on
their right edge.

Foreign labels have about 6 lines, 29 characters wide worth of space on their
right edge.

"""

import os
import datetime
from io import BytesIO
import textwrap
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader


path = os.environ['PRIVATE_DATA'] + '/ebay/12-labels.pdf'
chunk = '12346789 '
domestic = textwrap.fill(chunk * 12, 39)
foreign = textwrap.fill(chunk * 18, 29)


def main():
    reader = PdfFileReader(open(path, 'rb'))
    pages = [reader.getPage(i) for i in range(reader.numPages)]

    # Write pages to output file.
    writer = writer = PdfFileWriter()
    for page in pages[:5]:
        add_message(page, content=domestic, translate=(411, 325), rotate=180)
        add_message(page, content=domestic, translate=(411, 722), rotate=180)
        writer.addPage(page)

    page6 = pages[5]
    add_message(page6, content=domestic, translate=(411, 325), rotate=180)
    writer.addPage(page6)

    page7 = pages[6]
    add_message(page7, content=foreign, translate=(537, 143), rotate=-90)
    writer.addPage(page7)

    with open('output.pdf', 'wb') as fp:
        writer.write(fp)


def add_message(page, content, translate, rotate=0):
    inch = 72
    buf = BytesIO()
    c = Canvas(buf, pagesize=(11*inch, 8.5*inch))

    x, y = translate
    y = 11*inch - y
    c.translate(x, y)
    if rotate != 0:
        c.rotate(rotate)

    t = c.beginText()
    t.setFont('Courier', 8)
    t.setTextOrigin(0, 0)
    t.textLines(content)
    c.drawText(t)

    c.save()

    text_page = PdfFileReader(buf).getPage(0)
    page.mergePage(text_page)


if __name__ == '__main__':
    main()