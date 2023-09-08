import numpy as np
import numpy.linalg as la
import scipy.spatial as spat
from scipy.spatial.transform import Rotation as R
from p5 import *

points =0.75*np.array([[50, 0, 200], [-50, 0, 200], [0, 50, 300], [50, 0, 200], [0, -50, 300], [0, 50, 300], [0, -50, 300], [50, 0, 200], [0, -50, 300], [-50, 0, 200]])

def toSphere(fst, sec):
    begin_shape()
    d = sec-fst
    for i in range(20):
        inc = d/20*i
        plt = (fst + inc)/la.norm(fst+inc)*100
        vertex(plt[0], plt[1], plt[2])

    end_shape()




def setup():
    #noFill()
    size(1000, 1000)
    frame_rate=5

def draw():

    background(120)
    camera(4*(mouse_x-width/2), 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0)

    push()
    stroke(255, 0, 0)
    noFill()
    sphere(100)
    pop()

    push()
    noFill()
    stroke_weight(10)
    begin_shape()
    for pt in points:
        vertex(pt[0], pt[1], pt[2])
    end_shape(CLOSE)
    pop()

    push()
    noFill()
    stroke(255)
    for n, i in enumerate(points):
        toSphere(i, points[(n+1)%len(points)])
    pop()

if __name__ == '__main__':
    run(mode='P3D')


