import os
from PyPDF2 import PdfFileReader

# path = 'input.pdf'

# Probably will not be able to extract text from this document.
path = os.environ['PRIVATE_DATA'] + '/ebay/12-labels.pdf'

reader = PdfFileReader(path)
page = reader.getPage(0)
print(page.extractText())
