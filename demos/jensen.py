#   contracting the long edges of a jensen icosahedron until it morphs into a regular
#   octahedron. 
#
#   showing both planar and spherical projections of vertices.

import sys
import os
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from classes.graph import *
from classes.node import *
           
A = Node([], [200, 100, 0])       
B = Node([], [-200, 100, 0])       
C = Node([], [200, -100, 0])       
D = Node([], [-200, -100, 0])       
E = Node([], [0, 200, 100])
F = Node([], [0, -200, 100])
G = Node([], [0, 200, -100])
H = Node([], [0, -200, -100])
I = Node([], [100, 0, 200])
J = Node([], [100, 0, -200])
K = Node([], [-100, 0, 200])
L = Node([], [-100, 0, -200])

A.adjacencies = [B, I, J, E, G]
B.adjacencies = [L, G, A, E, K]
C.adjacencies = [I, J, F, H, D]
D.adjacencies = [K, L, C, H, F]
E.adjacencies = [A, B, I, K, F]
F.adjacencies = [E, C, D, I, K]
G.adjacencies = [H, A, B, J, L]
H.adjacencies = [G, C, D, J, L]
I.adjacencies = [J, A, C, E, F]
J.adjacencies = [I, A, C, G, H]
K.adjacencies = [L, B, D, E, F]
L.adjacencies = [K, B, D, G, H]

jensen = Graph([A, B, C, D, E, F, G, H, I, J, K, L])


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

    background(120)
    no_fill()
    camera(4*(mouse_x-width/2), 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0)

    """if(count == 10):
        inc = 1/inc
        count = 0
    count += 1"""
    push()
    stroke(120, 0, 0)
    #sphere(99)
    pop()
    
    if(count < 100):
        jensen.contract(0, 1)
        jensen.contract(2, 3)
        jensen.contract(4, 5)
        jensen.contract(6, 7)
        jensen.contract(8, 9)
        jensen.contract(10, 11)
        #jensen.translate(t)
        count += 1

   
    push()
    begin_shape()
    #grap.plot()
    stroke(0)
    stroke_weight(100)
    jensen.plot()
    end_shape()
    pop()
    
    kernel = jensen.kernel()


    push()
    stroke(255)
    #grap.plotSpherical(100)
    jensen.plotSpherical(100)
    pop()

    push()
    stroke(255, 0, 0)
    #square.projectToPlane()
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
    plane(10000, 10000)
    pop()

if __name__ == '__main__':
    run(mode='P3D')
