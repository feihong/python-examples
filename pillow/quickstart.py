from PIL import Image, ImageDraw


im = Image.new('RGB', (320, 240), 'red')

draw = ImageDraw.Draw(im)
draw.rectangle([10, 10, 310, 230], fill='black')
del draw

im.save('test.png')
