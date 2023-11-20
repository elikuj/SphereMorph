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

# tri examples
original = np.array([
[0.595355102726887, 0.1505149173145889, 0.7892385959409489],
[-0.5303423803002939, 0.44785231238251605, 0.7198369717867037],
[-0.05131058736352181, -0.06915713352329823, -0.9962853579709234],
])
badex = np.array([
[0.6855378087361367, 0.17331449100769447, 0.7071067811865475],
[-0.5402469002970622, 0.45621627187049796, 0.7071067811865475],
[-0.4213298158392842, -0.5678742697858699, -0.7071067811865475],
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


