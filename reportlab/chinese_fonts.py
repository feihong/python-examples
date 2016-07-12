from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen.canvas import Canvas


pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
inch = 72


TEXTS = [
    '你好世界！',
    '我们聊得很开心，不是吗？',
    '那个亡灵让我觉得毛骨悚然',
    '选举快到了！你会投谁？',
    'Party Pooper',
]


def draw_string(x, y, text):
    c.drawString(x * inch, y * inch, text)


with open('test.pdf', 'wb') as fp:
    c = Canvas(fp, pagesize=(8.5*inch, 11*inch))

    c.setFont('STSong-Light', 32)
    for y in range(10, 0, -1):
        if not TEXTS:
            break
        draw_string(1, y, TEXTS.pop())
        print(TEXTS)

    c.showPage()
    c.save()
