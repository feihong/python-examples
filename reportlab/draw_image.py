"""
Create a new PDF file that contains an image.

"""
from reportlab.pdfgen.canvas import Canvas


inch = 72


with open('output.pdf', 'wb') as fp:
    c = Canvas(fp, pagesize=(11*inch, 8.5*inch))
    c.setFillColorRGB(1, 0, 0)
    c.rect(0, 0, 11*inch, 8.5*inch, fill=True)

    width, height = 4*inch, 6*inch
    img_file = '../pypdf2/label.png'

    # Don't draw the image at its native size, because it will take up way too
    # much space.
    dim = c.drawImage(img_file, 5, 100, width, height)
    print('Actual dimensions of image:', dim)

    c.drawImage(img_file, 10 + width, 100, width, height)
    c.drawImage(img_file, 15 + 2*width, 100, width, height)

    c.save()
