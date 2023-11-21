# code for plotting lemma 3 in p5 sim

import sys
import os
import data_structures as ds
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from classes.graph import *
from classes.node import *
from classes.p5Wrapper import *


# generating pi/4 and -pi/4 latitude circles
circ_coords = []
l_circ_coords = []
face = []
for i in range(0, 100):
    circ_coords.append(ds.coords((math.pi/4, math.pi*2*i/100)))
    face.append(i)
    
for i in range(0, 100):
    l_circ_coords.append(ds.coords((-math.pi/4, math.pi*2*i/100)))
    face.append(i)
    
circ_coords = np.array(circ_coords)
l_circ_coords = np.array(l_circ_coords)
face = np.array([face])
upper_circ = Graph(circ_coords, face)
lower_circ = Graph(l_circ_coords, face)

# tri examples. currently, bad examples from test run where phi \in [0, 2pi). (constraining to phi \in [0, pi) results in 100%(?) success rate.)
original = np.array([
[-0.2094031288098832, 0.03295911056791427, 0.9772737726324202],
[-0.6007552045303066, 0.22877596452802867, 0.7659991790361265],
[-0.022377682662482537, 0.03265576435491273, -0.9992161129470709],
])
badex = np.array([
[-0.6985075297467354, 0.10994194325694687, 0.7071067811865475],
[-0.6608130406495241, 0.25164682653975695, 0.7071067811865475],
[-0.39970860282441845, 0.5832949792584806, -0.7071067811865475],
])

og_graph = Graph(original, np.array([[0,1,2]]))
og_graph_static = Graph(original, np.array([[0,1,2]]))
new_graph = Graph(badex, np.array([[0,2,1]]))

tf = 0.01

def setup():
    #noFill()
    size(1000, 1000)
    frame_rate=2

def draw():
    """global count
    global inc
    global t"""
    #global twist
    global og_graph, tf


    background(120)
    no_fill()
    camera(4*(mouse_x-width/2), 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0)
    
    
    push()
    stroke(120, 0, 0)
    upper_circ.plotFromFaces(100)
    #circle(center, 100*math.sqrt(2)/2, mode="CENTER")
    pop()
    
    push()
    stroke(0, 0, 120)
    lower_circ.plotFromFaces(100)
    #circle(center, 100*math.sqrt(2)/2, mode="CENTER")
    pop()

    push()
    stroke(120, 0, 0)
    #sphere(99)
    pop()
    if tf < 1:
        tf += 0.001
        
    push()
    begin_shape()
    stroke(0)
    stroke_weight(100)
    og_graph_static.plotSphericalFromFaces(100)
    end_shape()
    pop()

   
    push()
    begin_shape()
    stroke(0)
    stroke_weight(100)
    og_graph.morph(new_graph, tf).plotSphericalFromFaces(100)
    end_shape()
    pop()

    push()
    stroke(255)
    begin_shape()
    new_graph.plotSphericalFromFaces(100)
    end_shape()
    pop()
    
    
    
    push()
    no_stroke()
    fill(120, 128)
    plane(10000, 10000)
    pop()

if __name__ == '__main__':
    run(mode='P3D')


