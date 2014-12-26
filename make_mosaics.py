import os

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from numpy import mean, ceil, floor, sqrt, zeros
from matplotlib.pyplot import imread

font = ImageFont.truetype("DejaVuSansMono-Bold.ttf",80)

classes = os.listdir('../data/train/')

try:
	os.mkdir('mosaics')
except OSError:
	pass

for cls in classes:    
    print cls
    fns = os.listdir('../data/train/{0}/'.format(cls))
    images = [imread('../data/train/{0}/{1}'.format(cls,fn)) for fn in fns]
    images = sorted(images, key=lambda im: im.shape[0])
    ncol = floor(sqrt(len(images)))
    meanw = mean([image.shape[1] for image in images]) + 10
    roww = ncol*meanw

    cls = cls.replace('_', ' ')
    
    mintitlew = min([font.getsize(w)[0] for w in cls.split()])
    maxtitlew = font.getsize(cls)
    
    if mintitlew > roww:
        roww = mintitlew
        title_lines = cls.split()
    else:
        title_lines = [cls,]
        
    y = 50
    x = 50
    for line in title_lines:
        w, h = font.getsize(line)
        x = max(x, w)
        y += h * 1.1

    roww = max(roww, x)
    
    titlew = x+100
    titleh = y+50
    
    
    i = 0
    row = 0
    col = 0
    maxX = 0
    maxY = 0

    y = titleh+50
    while i < len(images):
        if col == 0:
            x = 50
            h = 0
        x += images[i].shape[1] + 10
        h = max(h, images[i].shape[0] + 10)

        i += 1
        col += 1
        if x > roww or i == len(images):
            col = 0
            y += h
            maxX = max(maxX, x)
            maxY = max(maxY, y)
    maxX = max(maxX, titlew)
    allim = zeros((maxY,maxX))

    i = 0
    row = 0
    col = 0

    y = titleh+50
    while i < len(images):
        if col == 0:
            x = 50
            h = 0

        allim[y:y+images[i].shape[0],x:x+images[i].shape[1]] = images[i]

        x += images[i].shape[1] + 10
        h = max(h, images[i].shape[0] + 10)

        i += 1
        col += 1
        if x > roww:
            col = 0
            y += h
        
    img = Image.fromarray(allim)
    draw = ImageDraw.Draw(img)

    y = 50
    x = 50
    for line in title_lines:
        draw.text((x, y),'{0}'.format(line),255,font=font)
        w, h = font.getsize(line)
        y += h * 1.1 
        
    img.convert('RGB').save('./mosaics/{0}.png'.format(cls.replace(' ', '_')), quality=100)
