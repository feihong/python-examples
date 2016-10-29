import datetime
from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader


def get_text_page():
    inch = 72
    bio = BytesIO()
    c = Canvas(bio, pagesize=(8.5*inch, 11*inch))

    c.setFillColor(HexColor(0xFF5722))
    text = 'Tiger, tiger, burning bright'
    c.drawString(5.5*inch, 10*inch, text)

    c.setFillColorRGB(1, 0, 1)
    c.translate(4.5*inch, 9*inch)
    c.rotate(-90)
    text = 'Hey Jude, this was added at %s' % datetime.datetime.now()
    c.drawString(0, 0, text)
    c.save()
    return PdfFileReader(bio).getPage(0)


if __name__ == '__main__':
    reader = PdfFileReader(open('input.pdf', 'rb'))

    writer = PdfFileWriter()

    # Get first page from input document.
    page = reader.getPage(0)

    # Merge a page containing text into the input page.
    page.mergePage(get_text_page())

    # Add page to output document.
    writer.addPage(page)

    with open('output.pdf', 'wb') as fp:
        writer.write(fp)
