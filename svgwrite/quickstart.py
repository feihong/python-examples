from svgwrite import Drawing, rgb


dwg = Drawing('test.svg', size=(320, 240))
dwg.add(dwg.rect(insert=(10, 10), size=(300, 220), fill='blue'))
# dwg.add(dwg.line((0, 0), (320, 00), stroke='black'))
dwg.add(dwg.polyline(
    stroke='black',
    fill='none',
    stroke_width=5,
    points=[(0, 0), (320, 0), (320, 240), (0, 240), (0, 0)]
))
dwg.add(dwg.text(
    'Hello World',
    insert=(160, 120), text_anchor='middle', fill='yellow'
))
dwg.save()
