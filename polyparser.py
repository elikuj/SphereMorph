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

def parsePoly(filename, sf=100):

    #filename = "shapes/icosahedron.txt"
    #filename = "shapes/small-stellated-dodecahedron.txt"
    f = open(filename, "r")

    points = []
    faces = []
    #params = []
    param_count = 0
    scale_factor = sf

    # read file and convert to grap 
    for l in f:
        # !!! bug where if solid name starts with "C" or "V" this will throw a syntax error    
        if l[0] == "C":     # parameter
            ls = l.split(" = ")
            x = ls[0]
            exec("%s = %f" % (x, (eval(ls[-1][:-1].replace("sqrt", "math.sqrt")))))
    
            #params.append(getattr(sys.modules[__name__], f"C{param_count}"))
            #print(params)
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
        
    return Graph(points, faces)