from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from PyPDF2 import PdfFileWriter, PdfFileReader


text = """\
Tiger, tiger, burning bright
In the forests of the night,
What immortal hand or eye
Could frame thy fearful symmetry?

In what distant deeps or skies
Burnt the fire of thine eyes?
On what wings dare he aspire?
What the hand dare seize the fire?
"""


def get_text_page():
    inch = 72
    bio = BytesIO()
    c = Canvas(bio, pagesize=(11*inch, 8.5*inch))

    t = c.beginText()
    t.setFont('Helvetica', 14)
    t.setTextOrigin(2*inch, 6*inch)
    t.textLines(text)
    c.drawText(t)

    c.save()
    return PdfFileReader(bio).getPage(0)


if __name__ == '__main__':
    writer = PdfFileWriter()
    writer.addPage(get_text_page())
    writer.addMetadata({
        '/OrderID': '303203949-94293023',
        '/Items': 'anna, bianca, catrin',
        '/Buyer': 'cat_on_roof',
        '/BuyerMessage': 'Hold the hot peppers, please',
        '/Address': '4567 N Westeros Ln\nChicago, IL 60630',
    })
    with open('output.pdf', 'wb') as fp:
        writer.write(fp)
