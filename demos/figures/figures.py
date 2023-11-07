import numpy as np
import numpy.linalg as la
import scipy.spatial as spat
from scipy.spatial.transform import Rotation as R
from p5 import *

points =0.75*np.array([[50, 0, 200], [-50, 0, 200], [0, 50, 300], [50, 0, 200], [0, -50, 300], [0, 50, 300], [0, -50, 300], [-50, 0, 200]])

def toSphere(fst, sec, divs=20):
    begin_shape()
    d = sec-fst
    for i in range(divs):
        inc = d/divs*i
        plt = (fst + inc)/la.norm(fst+inc)*100
        vertex(plt[0], plt[1], plt[2])

    end_shape()


def swap_geodesic(fst, sec):
    # vector from midpoint to center of sphere:
    tocenter = -1*((fst + sec)/2)
    toSphere(fst, tocenter, divs=100)
    toSphere(tocenter, sec, divs=100)



def setup():
    #noFill()
    size(1000, 1000)
    frame_rate=5

def draw():

    background(255)
    camera(4*(mouse_x-width/2), 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0)

    push()
    stroke(255, 200, 255)
    noFill()
    sphere(98)
    pop()

    push()
    noFill()
    stroke_weight(10)
    begin_shape()
    stroke(150)
    for pt in points:
        vertex(pt[0], pt[1], pt[2])
    end_shape()
    pop()

    push()
    noFill()
    stroke(0)
    for n, i in enumerate(points):
        if n == 4:
            swap_geodesic(i, points[(n+1)%len(points)])
        elif n != 5:
            toSphere(i, points[(n+1)%len(points)])
    pop()

if __name__ == '__main__':
    run(mode='P3D')


