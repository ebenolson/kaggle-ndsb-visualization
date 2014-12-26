import scipy.optimize
import mec
from numpy import sqrt, max, mean, arange, pi, cos, sin, array
from numpy.random import randint

def pack_circles(rs):
    N = len(rs)
    scale = mean(rs)
    rs = array(rs)/scale

    def func(p):
        xs = p[N:]
        ys = p[:N]
        dists = (sqrt(xs**2+ys**2)+rs)
        return max(dists) + mean(dists)

    cons = ()
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            cons += (eval('lambda p: (p[{0}]-p[{1}])**2+(p[{2}]-p[{3}])**2 - ({4})**2'.format(i,j,N+i,N+j,rs[i]+rs[j])),)
            
    p0 = randint(-max(rs)*10,max(rs)*10,N*2)
    p = scipy.optimize.fmin_slsqp(func, p0, ieqcons=cons, iter=5000, iprint=0)
    
    ys = p[:N]
    xs = p[N:]

    pts = []
    for i in range(len(rs)):
        for theta in arange(0,2*pi,2*pi/180):
            pts.append((xs[i]+rs[i]*cos(theta), ys[i]+rs[i]*sin(theta)))
    x0, y0, rb = mec.make_circle(pts)

    ys -= y0
    xs -= x0
    
    return xs*scale, ys*scale, rb*scale
