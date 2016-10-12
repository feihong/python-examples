from svgwrite import Drawing, rgb


bg_color = rgb(0, 188, 212)
bg_color2 = rgb(0, 151, 167)
text_color = '#333'


dwg = Drawing('test.svg', size=(320, 240))
dwg.add(dwg.rect(insert=(0, 0), size=(320, 240), fill=bg_color2))
dwg.add(dwg.rect(insert=(20, 20), size=(280, 200), fill=bg_color))
# dwg.add(dwg.line((0, 0), (320, 00), stroke='black'))
dwg.add(dwg.polyline(
    stroke='black',
    fill='none',
    stroke_width=5,
    points=[(0, 0), (320, 0), (320, 240), (0, 240), (0, 0)]
))
dwg.add(dwg.text(
    '莫问',
    fill=text_color,
    insert=(160, 100), text_anchor='middle', font_size=40
))
dwg.add(dwg.text(
    '歌手：红料',
    fill=text_color,
    insert=(160, 150), text_anchor='middle', font_size=32,
))
dwg.save()
