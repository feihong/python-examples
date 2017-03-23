import os
import textwrap
from PyPDF2 import PdfFileWriter, PdfFileReader

from common import add_message, add_rect


path = os.environ['PRIVATE_DATA'] + '/ebay/single-domestic.pdf'
packing = textwrap.fill('M' * 28 * 2, 28)
notes = textwrap.fill('M' * 83 * 4, 83)

reader = PdfFileReader(open(path, 'rb'), strict=False)
page1 = reader.getPage(0)

writer = PdfFileWriter()
add_message(page1, content=packing, translate=(223, 318))
add_rect(page1, (25, 340, 505, 49))
add_message(page1, content=notes, translate=(29, 350))

writer.addPage(page1)

with open('output.pdf', 'wb') as fp:
    writer.write(fp)
