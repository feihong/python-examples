"""
Create a new PDF file that merges two other PDF files into it.

"""
import datetime
from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from PyPDF2 import PdfFileWriter, PdfFileReader


inch = 72


def get_new_page():
    bio = BytesIO()
    c = Canvas(bio, pagesize=(11*inch, 8.5*inch))
    c.showPage()
    c.save()
    reader = PdfFileReader(bio)
    return reader.getPage(0)


def add_label(page, x, y):
    fp = open('label.pdf', 'rb')
    reader = PdfFileReader(fp)
    page.mergeTranslatedPage(reader.getPage(0), x, y)


def add_text(page):
    items = '4-dork-9, 3-dweeb-5'

    bio = BytesIO()
    c = Canvas(bio, pagesize=(11*inch, 8.5*inch))
    c.setFont('Helvetica', 12)
    c.drawString(inch, 120, 'User: CoolioFoolio')
    c.drawString(inch, 100, 'Tracking number: 0000 1111 2222 3333 4444 5555 66')
    c.drawString(inch, 80, 'Items: ' + items)

    c.setFont('Helvetica', 9)
    c.translate(250, 450)
    c.rotate(-90)
    c.drawString(0, 0, items)
    c.save()
    reader = PdfFileReader(bio)
    page.mergePage(reader.getPage(0))


if __name__ == '__main__':
    output = PdfFileWriter()
    page = get_new_page()
    output.addPage(page)

    add_label(page, -10, 2*inch)
    add_label(page, 253, 2*inch)
    add_label(page, 515, 2*inch)

    add_text(page)

    with open('output.pdf', 'wb') as fout:
        output.write(fout)
