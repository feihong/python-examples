from PyPDF2 import PdfFileReader


reader = PdfFileReader('input.pdf')
page = reader.getPage(0)
print(page.extractText())
