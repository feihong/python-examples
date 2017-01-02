import os
from pathlib import Path
from PyPDF2 import PdfFileWriter, PdfFileReader

path = Path('../../private-data/ebay/labels.pdf')
input_pdf = PdfFileReader(path.open('rb'))

for i in range(input_pdf.numPages):
    writer = PdfFileWriter()
    writer.addPage(input_pdf.getPage(i))
    with open('page-%d.pdf' % i, 'wb') as fp:
        writer.write(fp)
