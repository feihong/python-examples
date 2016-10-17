"""
Create a new PDF file that contains an image.

"""
from reportlab.pdfgen.canvas import Canvas


inch = 72


with open('output.pdf', 'wb') as fp:
    c = Canvas(fp, pagesize=(11*inch, 8.5*inch))
    c.setStrokeColorRGB(0.4, 0.4, 0.4)
    c.setFillColorRGB(1, 0, 0)
    c.rect(10, 10, 11*inch-20, 8.5*inch-20, fill=True)

    c.drawImage('../pypdf2/label.png', 0, 0, 100, 300)
    c.save()
