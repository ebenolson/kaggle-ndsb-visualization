import os, sys
import pickle

from PIL import Image

from numpy import array, tile, sqrt, ceil, floor, zeros, arange
from matplotlib.pyplot import imread

import circlepack

#############################################################
## Calculate bubble hierachy and positions from taxonomy file
#############################################################

f = open("taxonomy.txt", "r")

depth = 0
root = { "name": "root", "children": [] }
parents = []
node = root
for line in f:
    line = line.rstrip()
    newDepth = len(line) - len(line.lstrip("\t")) + 1
    # if the new depth is shallower than previous, we need to remove items from the list
    if newDepth < depth:
        parents = parents[:newDepth]
    # if the new depth is deeper, we need to add our previous node
    elif newDepth == depth + 1:
        parents.append(node)
    # levels skipped, not possible
    elif newDepth > depth + 1:
        raise Exception("Invalid file")
    depth = newDepth

    # create the new node
    node = {'name': line.strip().replace(' ', '_'), 'depth': depth, 'children':[]}
    # add the new node into its parent's children
    parents[-1]["children"].append(node)

def calc_bubbles(d):
    if 'children' in d:
        if d['children'] == []:
            d.pop('children')
            h, w, _ = imread('./mosaics/{0}.png'.format(d['name'])).shape
            d['radius'] = sqrt(h**2/4 + w**2/4)
            print 'Bubbled {0}'.format(d["name"])
            return d["name"]
        else:
            for child in d["children"]:
                calc_bubbles(child)
            rs = [child['radius'] for child in d['children']]
            ys, xs, rb = circlepack.pack_circles(rs)
            d['radius'] = rb
            for y, x, child in zip(ys, xs, d['children']):
                child['x'] = x
                child['y'] = y 

calc_bubbles(root)

root['x'] = 0
root['y'] = 0
root['depth'] = 0

pickle.dump(root, open('bubbles.pickle','w'))

###################################
## Render bubbles and mosaic images
###################################

TILEW = 1024
NTILES = int(ceil(root['radius']*2/TILEW))
out = zeros((NTILES*TILEW, NTILES*TILEW, 3), dtype='uint8')
out[:,:,:] = 255

fullx = arange(out.shape[0])
fullx = fullx-fullx.mean()
fully = fullx

def render_circle(x0, y0, r0, color):
    r02 = r0**2
    for i in range(NTILES):
        for j in range(NTILES):
            tileRmin = sqrt((fullx[i*TILEW]-x0)**2 + (fully[j*TILEW]-y0)**2) - sqrt(TILEW**2 * 2)
            tileRmax = sqrt((fullx[i*TILEW]-x0)**2 + (fully[j*TILEW]-y0)**2) + sqrt(TILEW**2 * 2)
            if tileRmin > r0:
                continue
            if tileRmax < r0:
                out[j*TILEW:(j+1)*TILEW, i*TILEW:(i+1)*TILEW] = color
                continue
            tilex = fullx[i*TILEW:(i+1)*TILEW]
            tiley = fully[j*TILEW:(j+1)*TILEW]
            r2 = (tile(tilex,(1024,1))-x0)**2 + (tile(tiley,(1024,1))-y0).T**2
            out[j*TILEW:(j+1)*TILEW, i*TILEW:(i+1)*TILEW][r2<=r02] = color

def render_bubbles(d, x=0, y=0):
    if 'name' in d:
        print 'Drawing bubble for {0}'.format(d['name'])
        sys.stdout.flush()
        
    x = x+d['x']
    y = y+d['y']
    r = d['radius']
    c = array([0,d['depth']*0.1+0.2,d['depth']*0.1+0.3])*255

    render_circle(x, y, r, c)
    if 'children' in d:
        for child in d['children']:
            render_bubbles(child,x,y)

def render_image(d, x=0, y=0):
    x = x+d['x']
    y = y+d['y']
    r = d['radius']
    
    if 'children' in d:
        for child in d['children']:
            render_image(child,x,y)
    else:
        print 'Drawing image for {0}'.format(d['name'])
        im = imread('./mosaics/{0}.png'.format(d['name']))
        im = (im*255).astype('uint8')
        h, w, _ = im.shape
        out[y-floor(h/2.):y+ceil(h/2.), x-floor(w/2.):x+ceil(w/2.), :] = im

render_bubbles(root)
render_image(root, x=out.shape[1]//2, y=out.shape[0]//2)

def downsample(image):
    h, w, _ = image.shape
    for x in arange(w)[::2]:
        if x+1 < w:
            image[:,x,:] = ((image[:,x,:].astype('uint16')+image[:,x+1,:].astype('uint16'))//2).astype('uint8')
        else:
            image[:,x,:] = ((image[:,x,:].astype('uint16')+image[:,x-1,:].astype('uint16'))//2).astype('uint8')
    for y in arange(h)[::2]:
        if y+1 < h:
            image[y,:,:] = ((image[y,:,:].astype('uint16')+image[y+1,:,:].astype('uint16'))//2).astype('uint8')
        else:
            image[y,:,:] = ((image[y,:,:].astype('uint16')+image[y-1,:,:].astype('uint16'))//2).astype('uint8')
    return image[::2,::2]

#############################
## Write tile pyramid to disk
#############################

TILE_SIZE=256
zoom = 0
while 1:
    print 'Writing zoom level {0}'.format(zoom)
    try:
        os.makedirs('pyramid/zoom%d/'%(20-zoom))
    except:
        pass
    h, w, _ = out.shape
    nx = int(ceil(w*1.0/TILE_SIZE))
    ny = int(ceil(h*1.0/TILE_SIZE))
    for i in range(nx):
        for j in range(ny):
            oi = zeros((TILE_SIZE,TILE_SIZE,3), dtype='uint8')
            oi[:,:,:] = 255
            x0 = i*TILE_SIZE
            y0 = j*TILE_SIZE
            x1 = min((i+1)*TILE_SIZE, w)
            y1 = min((j+1)*TILE_SIZE, h)
            oi[0:y1-y0,0:x1-x0,:] = out[y0:y1,x0:x1,:]
            Im = Image.fromarray(oi)
            Im.save('pyramid/zoom%d/%d-%d.png'%(20-zoom,i,j))
    
    if nx <= 3 and ny <= 3 and zoom >= 2:
        break
        
    zoom += 1
    out = downsample(out)    
