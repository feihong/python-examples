from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen.canvas import Canvas


pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

point = 1
inch = 72


c = Canvas('test.pdf', pagesize=(8.5 * inch, 11 * inch))
c.setStrokeColorRGB(0,0,0)
c.setFillColorRGB(0,0,0)
# c.setFont('Helvetica', 12 * point)
c.drawString(1*inch, 10*inch, 'Hello World')

c.setFont('STSong-Light', 32*point)
c.drawString(3*inch, 9*inch, 'Poop')
c.drawString(3*inch, 8*inch, '你好世界！')

c.showPage()
c.save()
