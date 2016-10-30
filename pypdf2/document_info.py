import os
from pprint import pprint
from PyPDF2 import PdfFileReader


def print_pdf_metadata(filename):
    reader = PdfFileReader(open(filename, 'rb'))
    pprint(reader.documentInfo)


if __name__ == '__main__':
    filenames = ['input.pdf', 'label.pdf', 'output.pdf']
    for filename in os.listdir('.'):
        if filename.endswith('.pdf'):
            print(filename, '\n')
            print_pdf_metadata(filename)
            print('='*75)
