# parser to convert a shape from http://dmccooey.com/polyhedra/index.html to a graph object and plot with p5

import numpy as np
import numpy.linalg as la
import math
import sys
import os
import p5
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from classes.graph import *
from classes.node import *

filename = "small-stellated-dodecahedron.txt"

f = open(filename, "r")

points = []
params = []
param_count = 0
scale_factor = 300

for l in f:
    if l[0] == "C":     # parameter
        ls = l.split(" = ")
        x = ls[0]
        exec("%s = %f" % (x, (eval(ls[-1][:-1].replace("sqrt", "math.sqrt")))))
        params.append(getattr(sys.modules[__name__], f"C{param_count}"))
        print(params)
        param_count += 1
        
    if l[0] == "V":     # vertex
        points.append(Node([], scale_factor *np.array(eval(l.strip().split("=")[-1].replace("(", "[").replace(")", "]")))))
        print(points[-1].coordinates)
    if l[0] == "{":     # face
        edges = eval(l.strip().replace("{", "[").replace("}", "]"))
        for i in range(len(edges)):
            points[edges[i]].adjacencies.append(points[edges[(i+1)%len(edges)]])
    
    
shape = Graph(points)



#shape.scale(100)
# plotting the imported shape


def setup():
    fill(0, 0, 0)
    size(1000, 1000)
    frame_rate=2

def draw():
    background(120)
    no_fill()
    camera(4*(mouse_x-width/2), 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0)




    push()
    stroke(120, 0, 0)
    sphere(99)
    pop()

   
    push()
    begin_shape()
    stroke(0)
    stroke_weight(100)
    shape.plot()
    end_shape()
    pop()


    push()
    stroke(255)
    shape.plotSpherical(100)
    pop()

    push()  
    stroke(255, 0, 0)
    #square.projectToPlane()
    pop()

    push()
    no_stroke()
    fill(120, 128)
    plane(10000, 10000)
    pop()

if __name__ == '__main__':
    run(mode='P3D')
