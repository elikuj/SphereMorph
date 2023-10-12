#   playing with trying to average the points on the graph idk

import sys
import os
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from classes.graph import *
from classes.node import *
           
A = Node([], (0, 0, 0))
B = Node([], (1, 0, 0))
C = Node([], (0.5, 1, 0))
D = Node([], (-0.5, 1, 0))
E = Node([], (0, 2, 0))
F = Node([], (0, 1, 1))
G = Node([], (1, 1, 1))
H = Node([], (-1, 1, 1))
I = Node([], (0, 0, 2))
J = Node([], (0, -1, 1))
K = Node([], (1, -1, 1))
L = Node([], (-1, -1, 1))
M = Node([], (0, 0, 3))

A.adjacencies = [B, C, D]
B.adjacencies = [A, C, E]
C.adjacencies = [A, B, D, F]
D.adjacencies = [A, C, E, H]
E.adjacencies = [B, D, F]
F.adjacencies = [C, E, G, H]
G.adjacencies = [F, H, I]
H.adjacencies = [D, F, G, I]
I.adjacencies = [G, H, J, K]
J.adjacencies = [I, K, L]
K.adjacencies = [I, J, L, M]
L.adjacencies = [J, K, M]
M.adjacencies = [K, L]

grap = Graph([A, B, C, D, E, F, G, H, I, J, K, L, M])


def stretchmat(factor):
    return np.array([[factor, 0, 0], [0, 1, 0], [0, 0, 1]])

count = 0
inc = 1.5

a = Node([], (50, 50, 100))
b = Node([], (-50, 50, 100))
c = Node([], (50, -50, 100))
d = Node([], (-50, -50, 100))
e = Node([], (50, 50, 200))
f = Node([], (-50, 50, 200))
g = Node([], (50, -50, 200))
h = Node([], (-50, -50, 200))

a.adjacencies = [b, e, c]
b.adjacencies = [a, f, d]
c.adjacencies = [a, d, g]
d.adjacencies = [b, h, c]
e.adjacencies = [a, g, f]
f.adjacencies = [e, b, h]
g.adjacencies = [e, c, h]
h.adjacencies = [d, g, f]

square = Graph([a, b, c, d, e, f, g, h])

count = 0

t = np.array([1, 1, 1])


def setup():
    #noFill()
    size(1000, 1000)
    frame_rate=2

def draw():
    global count
    global inc
    global t

    background(120)
    no_fill()
    camera(4*(mouse_x-width/2), 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0)

    if(count <= 10):
        square.soften()
    count += 1


    push()
    stroke(120, 0, 0)
    sphere(99)
    pop()

   
    push()
    begin_shape()
    stroke(0)
    stroke_weight(100)
    square.plot()
    end_shape()
    pop()


    push()
    stroke(255)
    square.plotSpherical(100)
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
