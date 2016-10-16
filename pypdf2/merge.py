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


def merge_label(page):
    fp = open('label.pdf', 'rb')
    reader = PdfFileReader(fp)
    page.mergeTranslatedPage(reader.getPage(0), inch, 2*inch)
    

if __name__ == '__main__':
    output = PdfFileWriter()
    page = get_new_page()
    output.addPage(page)

    merge_label(page)

    with open('output.pdf', 'wb') as fout:
        output.write(fout)
