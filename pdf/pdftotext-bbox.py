import os
import subprocess
from PyPDF2 import PdfFileReader

# Probably will not be able to extract text from this document.
path = os.environ['PRIVATE_DATA'] + '/ebay/12-labels.pdf'

cmd = [
    'pdftotext',
    str(path),
    '-f', '1',    # first page
    '-l', '1',    # last page
    '-bbox',
    'output.html',
]
text = subprocess.check_output(cmd).decode('utf-8')
print(text)
