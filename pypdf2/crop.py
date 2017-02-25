"""
Crop the contents of label.pdf and output the results to cropped_label.pdf.

Source: http://stackoverflow.com/questions/457207/cropping-pages-of-a-pdf-file

"""
import datetime
from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from PyPDF2 import PdfFileWriter, PdfFileReader


def get_label_page():
    fp = open('label.pdf', 'rb')
    # Set strict to False because document may not have unique keys.
    reader = PdfFileReader(fp, strict=False)
    page = reader.getPage(0)
    page.mediaBox.lowerLeft = (15, 10)
    page.mediaBox.upperRight = (273, 433)
    # page.cropBox.lowerLeft = (15, 10)
    # page.cropBox.upperRight = (273, 457)
    # page.trimBox.lowerLeft = (15, 10)
    # page.trimBox.upperRight = (273, 457)
    return page


if __name__ == '__main__':
    output = PdfFileWriter()
    output.addPage(get_label_page())

    with open('cropped_label.pdf', 'wb') as fout:
        output.write(fout)
