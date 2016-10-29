"""
Copy an image from one pdf file to another.

"""
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas


def get_images(pdf_file):
    with open(pdf_file, 'rb') as fp:
        reader = PdfFileReader(fp)
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


def get_image_page(image):
    inch = 72
    bio = BytesIO()
    c = Canvas(bio, pagesize=(8.5*inch, 11*inch))
    # c.drawImage(img_file, x, 100, width, height)
    c.drawImage(image, 0, 50, 4*inch, 6*inch)
    c.save()
    return PdfFileReader(bio).getPage(0)


if __name__ == '__main__':
    image = list(get_images('label.pdf'))[0]
    image_reader = ImageReader(image)

    with open('output.pdf', 'wb') as fp:
        writer = PdfFileWriter()
        writer.addPage(get_image_page(image_reader))
        writer.write(fp)
