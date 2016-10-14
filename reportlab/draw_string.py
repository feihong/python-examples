"""
Create a letter size canvas and draw some strings on it.

"""

from reportlab.pdfgen.canvas import Canvas


point = 1
inch = 72


with open('output.pdf', 'wb') as fp:
    c = Canvas(fp, pagesize=(8.5*inch, 11*inch))
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    c.setFont('Helvetica', 12 * point)

    y = 10
    for i in range(1, 38):
        if i == 12:
            c.setFillColorRGB(1,0,0)
            text = "%d. Oh no, there's a ghost behind you!!!" % i
        else:
            c.setFillColorRGB(0,0,0)
            text = '%d. I must not fear. Fear is the mind killer.' % i
        c.drawString(1 * inch, y * inch, text)
        y -= 0.25

    c.showPage()
    c.save()
