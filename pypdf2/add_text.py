from io import StringIO
from PyPDF2 import PdfFileWriter, PdfFileReader


def get_text_doc(x, y, text):
    inch = 72
    sio = StringIO()
    c = Canvas(sio, pagesize=(8.5*inch, 11*inch))
    c.drawString(4*inch, 5*inch, 'Added text')
    c.save()
    return PdfFileReader(sio)


if __name__ == '__main__':
    with open('input.pdf', 'rb') as fp:
        input1 = PdfFileReader(fp)

        output = PdfFileWriter()
        output.addPage(input1.getPage(0))

        output.addBlankPage()

        with open('output.pdf', 'wb') as fout:
            output.write(fout)
