from PIL import Image, ImageDraw, ImageFont


im = Image.new('RGB', (320, 240), 'red')

draw = ImageDraw.Draw(im)
draw.rectangle([10, 10, 310, 230], fill='white')

draw.text((20, 80), 'Hello World', fill='black')
del draw

im.save('test.png')
