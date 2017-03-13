import os
import textwrap
from PyPDF2 import PdfFileWriter, PdfFileReader
from common import add_message


path = os.environ['PRIVATE_DATA'] + '/ebay/12-labels.pdf'
chunk = '12346789 '
# chunk = 'MMMMMMMM '
domestic = textwrap.fill(chunk * 6, 32)
foreign = textwrap.fill(chunk * 10, 23)
domestic_notes = textwrap.fill(chunk * 24, 73)
foreign_notes = textwrap.fill(chunk * 24, 79)
center_line = '-  ' * 30
user = 'User: blarney-stone-bear-9381'


reader = PdfFileReader(open(path, 'rb'))
pages = [reader.getPage(i) for i in range(reader.numPages)]


# Write pages to output file.
writer = PdfFileWriter()
for i, page in enumerate(pages[:5], 1):
    add_message(page, content=domestic, translate=(244, 316))
    add_message(page, content=domestic_notes, translate=(100, 347))
    add_message(page, content=center_line, translate=(45, 397))
    add_message(page, content=domestic, translate=(244, 713))
    add_message(page, content=domestic_notes, translate=(100, 425))
    add_message(page, content=user, translate=(45, 760))
    add_message(page, content='Page 10{} of 800'.format(i), translate=(470, 760))

    writer.addPage(page)

page6 = pages[5]
add_message(page6, content=domestic, translate=(244, 316))
writer.addPage(page6)

page7 = pages[6]
add_message(page7, content=foreign, translate=(537, 143), rotate=-90)
add_message(page7, content=foreign_notes, translate=(75, 645))
writer.addPage(page7)

with open('output.pdf', 'wb') as fp:
    writer.write(fp)
