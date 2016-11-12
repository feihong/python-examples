"""
To conver the resulting svg file to png, run:

convert test.svg test.png

"""
from svgwrite import Drawing, rgb

color1 = '#ff5722'
color2 = '#222'

width, height = 800, 200
dwg = Drawing('test.svg', size=(width, height))
dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=color2))
dwg.add(dwg.text(
    '骑虎难下',
    fill=color1,
    insert=(width/2, height/2 + 30), text_anchor='middle', font_size=80
))
dwg.save()
