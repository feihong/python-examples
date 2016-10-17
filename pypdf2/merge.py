"""
Create a new PDF file that combines images and text.

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


def add_labels(page, coordinates):
    bio = BytesIO()
    c = Canvas(bio, pagesize=(11*inch, 8.5*inch))
    width, height = 3.6*inch, 5.4*inch

    for x, y in coordinates:
        c.drawImage('label.png', x, y, width, height)
        c.rect(x, y, width, height)

    c.save()
    page2 = PdfFileReader(bio).getPage(0)
    page.mergePage(page2)



def add_text(page):
    items = '4-dork-9, 3-dweeb-5'

    x = 3

    bio = BytesIO()
    c = Canvas(bio, pagesize=(11*inch, 8.5*inch))
    c.setFont('Helvetica', 10)
    lines = [
        'User: CoolioFoolio',
        'Tracking number: 0000 1111 2222 3333 4444 5555 66',
        'Items: ' + items,
    ]
    for i, line in enumerate(lines):
        c.drawString(x, 120 - i*15, line)

    c.setFont('Helvetica', 8)
    c.translate(255, 443)
    c.rotate(-90)
    c.drawString(0, 0, items)
    c.save()
    reader = PdfFileReader(bio)
    page.mergePage(reader.getPage(0))


if __name__ == '__main__':
    output = PdfFileWriter()
    page = get_new_page()
    output.addPage(page)

    add_labels(page, [
        (3, 150),
        (265, 150),
        (527, 150),
    ])

    add_text(page)

    with open('output.pdf', 'wb') as fout:
        output.write(fout)
