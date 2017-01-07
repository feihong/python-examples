"""
Domestic labels have about three lines and 39 characters worth of space on
their right edge

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
content = textwrap.fill(chunk * 12, 39)
# content = chunk


def main():
    reader = PdfFileReader(open(path, 'rb'))
    pages = [reader.getPage(i) for i in range(reader.numPages)]

    # Write pages to output file.
    writer = writer = PdfFileWriter()
    for page in pages:
        add_message(page, content=content, translate=(411, 467), rotate=180)
        writer.addPage(page)
    with open('output.pdf', 'wb') as fp:
        writer.write(fp)


def add_message(page, content, translate, rotate):
    inch = 72
    buf = BytesIO()
    c = Canvas(buf, pagesize=(11*inch, 8.5*inch))

    c.translate(*translate)
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
