"""
Draw numbers in the four corners of the page

"""
from reportlab.pdfgen.canvas import Canvas


inch = 72


with open('output.pdf', 'wb') as fp:
    c = Canvas(fp, pagesize=(8.5*inch, 11*inch))

    c.setFontSize(10)
    c.drawString(0, 780, '1')
    c.drawString(605, 780, '2')
    c.drawString(605, 5, '3')
    c.drawString(0, 5, '4')
    c.save()
