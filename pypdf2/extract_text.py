import os
import subprocess
from PyPDF2 import PdfFileReader

reader = PdfFileReader('input.pdf')
page = reader.getPage(0)

text = page.extractText()
print(text)
