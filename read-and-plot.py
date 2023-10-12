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

filename = "shapes/icosahedron.txt"
#filename = "shapes/small-stellated-dodecahedron.txt"
# test
f = open(filename, "r")

points = []
faces = []
params = []
param_count = 0
scale_factor = 300

# read file and convert to grap 
for l in f:
    # !!! bug where if solid name starts with "C" or "V" this will throw a syntax error    
    if l[0] == "C":     # parameter
        ls = l.split(" = ")
        x = ls[0]
        exec("%s = %f" % (x, (eval(ls[-1][:-1].replace("sqrt", "math.sqrt")))))
        params.append(getattr(sys.modules[__name__], f"C{param_count}"))
        print(params)
        param_count += 1
        
    if l[0] == "V":     # vertex
        points.append(scale_factor *np.array(eval(l.strip().split("=")[-1].replace("(", "[").replace(")", "]"))))
        print(points[-1])
    if l[0] == "{":     # face
        edges = eval(l.strip().replace("{", "[").replace("}", "]"))
        #for i in range(len(edges)):
            #points[edges[i]].adjacencies.append(points[edges[(i+1)%len(edges)]])
        print(edges)
        faces.append(edges)
    
    
shape = Graph(points, faces)
kernel = shape.kernel()


#shape.scale(100)
# plotting the imported shape

prev_x = 0
prev_y = 0

def setup():
    #fill(0, 0, 0)
    size(1000, 1000)
    frame_rate=2
    

def draw():
    global prev_x, prev_y
    background(120)
    
    if mouse_is_pressed:
        
        prev_x = prev_x + (mouse_x - width/2)/(abs(mouse_x - width/2))*10
        prev_y = prev_y + (mouse_y - height/2)/(abs(mouse_y - height/2))*10
    camera(4*(prev_x-width/2), 4*(prev_y-height/2), (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0)



    # push()
    # stroke(120, 0, 0)
    # sphere(99)
    # pop()

   
    push()
    begin_shape()
    #fill(0,0,0)
    stroke(0)
    noFill()
    stroke_weight(200)
    shape.plotFromFaces()
    end_shape()
    pop()


    push()
    #blinn_phong_material()
    fill(100, 0, 0)
    
    stroke(255, 0, 0)
    kernel.plotFromFaces()
    
    
    pop()

    push()
    no_stroke()
    fill(120, 128)
    #plane(10000, 10000)
    pop()

if __name__ == '__main__':
    run(mode='P3D')
