import datetime
from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from PyPDF2 import PdfFileWriter, PdfFileReader


def get_text_page(x, y, text):
    inch = 72
    bio = BytesIO()
    c = Canvas(bio, pagesize=(8.5*inch, 11*inch))
    c.setFillColorRGB(1, 0, 0)
    c.drawString(x*inch, y*inch, text)
    c.save()
    reader = PdfFileReader(bio)
    return reader.getPage(0)


if __name__ == '__main__':
    with open('input.pdf', 'rb') as fp:
        input1 = PdfFileReader(fp)

        output = PdfFileWriter()

        # Add page from another document.
        output.addPage(input1.getPage(0))

        # Add page that was merged with another page.
        text_page = get_text_page(
            2.2, 10, 'Hey Jude, this was added at %s' % datetime.datetime.now())
        output.addPage(text_page)

        # Add an empty page
        output.addBlankPage()

        with open('output.pdf', 'wb') as fout:
            output.write(fout)
