from pprint import pprint
from PyPDF2 import PdfFileReader


if __name__ == '__main__':
    reader = PdfFileReader(open('input.pdf', 'rb'))
    pprint(reader.documentInfo)
