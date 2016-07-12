import datetime
from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from PyPDF2 import PdfFileWriter, PdfFileReader


def get_text_page(x, y, text):
    inch = 72
    bio = BytesIO()
    c = Canvas(bio, pagesize=(8.5*inch, 11*inch))
    c.setFillColorRGB(1, 0, 1)
    c.translate(x * inch, y * inch)
    c.rotate(-90)
    c.drawString(0, 0, text)
    c.save()
    reader = PdfFileReader(bio)
    return reader.getPage(0)


if __name__ == '__main__':
    with open('input.pdf', 'rb') as fp:
        input1 = PdfFileReader(fp)

        output = PdfFileWriter()

        # Generate a page that just contains some text.
        text_page = get_text_page(
            4.5, 9, 'Hey Jude, this was added at %s' % datetime.datetime.now())

        # Get first page from input document.
        page = input1.getPage(0)

        # Merge the text page into the input page.
        page.mergePage(text_page)

        # Add page to output document.
        output.addPage(page)

        with open('output.pdf', 'wb') as fout:
            output.write(fout)
