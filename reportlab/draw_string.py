from reportlab.pdfgen.canvas import Canvas

point = 1
inch = 72

c = Canvas('test.pdf', pagesize=(8.5 * inch, 11 * inch))
c.setStrokeColorRGB(0,0,0)
c.setFillColorRGB(0,0,0)
c.setFont('Helvetica', 12 * point)
c.drawString(1*inch, 10*inch, 'Hello World')

c.setFont('Courier', 32*point)
c.drawString(3*inch, 9*inch, 'Poop')

c.save()
