from reportlab.pdfgen.canvas import Canvas


point = 1
inch = 72


with open('test.pdf', 'wb') as fp:
    c = Canvas(fp, pagesize=(8.5*inch, 11*inch))
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    c.setFont('Helvetica', 12 * point)

    y = 10
    for i in range(1, 33):
        c.drawString(
            1 * inch,
            y * inch,
            '%d. I must not fear. Fear is the mind killer.' % i
        )
        y -= 0.3

    c.showPage()
    c.save()
