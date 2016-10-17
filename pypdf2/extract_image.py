"""
Extract an image from label.pdf.

Source: http://stackoverflow.com/a/34116472
"""
import PyPDF2

from PIL import Image


def get_images(pdf_file):
    with open(pdf_file, 'rb') as fp:
        reader = PyPDF2.PdfFileReader(fp)
        page = reader.getPage(0)
        xObject = page['/Resources']['/XObject'].getObject()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"

                encoding = xObject[obj]['/Filter']
                if encoding == '/FlateDecode':
                    yield Image.frombytes(mode, size, data)
                else:
                    raise Exception(
                        'Unexpected image encoding: {}'.format(encoding))


if __name__ == '__main__':
    image = list(get_images('label.pdf'))[0]
    image.save('label.png')
