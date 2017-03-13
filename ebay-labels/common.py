from io import BytesIO

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import white
from PyPDF2 import PdfFileReader


inch = 72


def add_message(page, content, translate, rotate=0):
    buf = BytesIO()
    canvas = Canvas(buf, pagesize=(8.5*inch, 11*inch))

    x, y = translate
    y = 11*inch - y
    canvas.translate(x, y)
    if rotate != 0:
        canvas.rotate(rotate)

    t = canvas.beginText()
    t.setFont('Courier', 10)
    t.setTextOrigin(0, 0)
    t.textLines(content)
    canvas.drawText(t)

    canvas.save()

    new_page = PdfFileReader(buf).getPage(0)
    page.mergePage(new_page)


def add_rect(page, bbox):
    """
    Add a white-filled rectangle with dashed border to the given page.

    """
    buf = BytesIO()
    canvas = Canvas(buf, pagesize=(8.5*inch, 11*inch))
    x, y, w, h = bbox
    y = 11*inch - y - h
    canvas.setFillColor(white)
    canvas.setLineWidth(0.1)
    canvas.setDash(3, 6)
    canvas.roundRect(x, y, w, h, 5, fill=True)
    canvas.save()
    new_page = PdfFileReader(buf).getPage(0)
    page.mergePage(new_page)
