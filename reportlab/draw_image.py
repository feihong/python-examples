"""
Create a new PDF file that contains an image.

"""
from reportlab.pdfgen.canvas import Canvas


inch = 72


with open('output.pdf', 'wb') as fp:
    c = Canvas(fp, pagesize=(11*inch, 8.5*inch))
    c.setStrokeColorRGB(0.4, 0.4, 0.4)
    c.setFillColorRGB(1, 0, 0)
    c.rect(0, 0, 11*inch, 8.5*inch, fill=True)

    dim = c.drawImage('../pypdf2/label.png', 10, 100, 1200/4, 1800/4)
    print(dim)
    c.save()
