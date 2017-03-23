import os
import textwrap
from PyPDF2 import PdfFileWriter, PdfFileReader

from common import add_message, add_rect


path = os.environ['PRIVATE_DATA'] + '/ebay/single-foreign-edited.pdf'
packing = textwrap.fill('M' * 16 * 5, 16)
notes = textwrap.fill('M' * 83 * 4, 83)

reader = PdfFileReader(open(path, 'rb'), strict=False)
page1 = reader.getPage(0)

writer = PdfFileWriter()
add_message(page1, content=packing, translate=(573, 165), rotate=-90)
add_message(page1, content=notes, translate=(102, 634))

writer.addPage(page1)

with open('output.pdf', 'wb') as fp:
    writer.write(fp)
