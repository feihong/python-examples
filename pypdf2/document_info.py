import os
from pathlib import Path
from pprint import pprint
from PyPDF2 import PdfFileReader


def print_pdf_metadata(path):
    reader = PdfFileReader(path.open('rb'))
    pprint(reader.documentInfo)


if __name__ == '__main__':
    files = Path('.').glob('*.pdf')
    files = list(files)
    files.append(Path(os.environ['PRIVATE_DATA']) / 'ebay/12-labels.pdf')

    for path in files:
        print(path, '\n')
        print_pdf_metadata(path)
        print('='*75)
