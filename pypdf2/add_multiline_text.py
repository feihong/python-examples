import datetime
from io import BytesIO
import textwrap
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader


chunk = '123456789 '
text = textwrap.fill(chunk * 12, 37)
# text = chunk * 4


def get_text_page():
    inch = 72
    bio = BytesIO()
    c = Canvas(bio, pagesize=(11*inch, 8.5*inch))

    x, y = 50, 50
    c.drawImage('label.png', x, y, 4*inch, 6*inch)
    c.rect(x, y, 4*inch, 6*inch)

    c.translate(330, 355)
    c.rotate(-90)

    t = c.beginText()
    t.setFont('Courier', 8)
    t.setTextOrigin(0, 0)
    t.textLines(text)
    c.drawText(t)

    c.save()
    return PdfFileReader(bio).getPage(0)


if __name__ == '__main__':
    writer = PdfFileWriter()
    writer.addPage(get_text_page())

    with open('output.pdf', 'wb') as fp:
        writer.write(fp)
