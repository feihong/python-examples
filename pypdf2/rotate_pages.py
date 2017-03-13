import os
from PyPDF2 import PdfFileWriter, PdfFileReader


input_path = os.environ['PRIVATE_DATA'] + '/ebay/bulk-mixed.pdf'
reader = PdfFileReader(open(input_path, 'rb'))
pages = (reader.getPage(i) for i in range(reader.numPages))

with open('output.pdf', 'wb') as fp:
    writer = PdfFileWriter()
    for page in pages:
        page.rotateCounterClockwise(90)
        writer.addPage(page)
    writer.write(fp)
