import sys
import os
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from classes.graph import *
from classes.node import *

# stolen from Jeff's code:

#  Parametrized twisted prism.
#       sides = number of sides (before twisting)
#       twist = amount of ccw twisting (in circles as the gods intended)
#       height = distance between top and bottom
#       radius = distance from center of top face to vertices of top face
#
#  The top and bottom facets of the prism are regular side-gons,
#       triangulated with one vertex in their centers.
#  Side faces are (top[i], bot[i], top[i+1]) and (bot[i], bot[i+1], top[i+1])
#
def TwistedPrism(sides=3, twist=1 / 12, height=2, radius=1):
    if twist > 1 / 2 - 1 / sides:
        print("❌DANGER❌ Self-intersecting twisted prism!")

    theta = np.linspace(0, 2 * np.pi, sides + 1)
    xbot = radius * np.cos(theta)
    ybot = radius * np.sin(theta)
    zbot = -height / 2
    xtop = radius * np.cos(theta - 2 * np.pi * twist)
    ytop = radius * np.sin(theta - 2 * np.pi * twist)
    ztop = height / 2

    botverts = [[xbot[i], ybot[i], zbot] for i in range(sides)]
    topverts = [[xtop[i], ytop[i], ztop] for i in range(sides)]
    vertices = np.array(botverts + topverts + [[0, 0, zbot], [0, 0, ztop]])

    botfaces = [[(i + 1) % sides, i, 2 * sides] for i in range(sides)]
    upfaces = [[i, (i + 1) % sides, sides + i] for i in range(sides)]
    dnfaces = [
        [(i + 1) % sides, sides + (i + 1) % sides, sides + i] for i in range(sides)
    ]
    topfaces = [
        [sides + i, sides + (i + 1) % sides, 2 * sides + 1] for i in range(sides)
    ]
    faces = np.array(botfaces + upfaces + dnfaces + topfaces)

    #SanityCheck(vertices, faces)  # ignore return value for now
    return (vertices, faces)



vtxs, faces = TwistedPrism(sides = 10, twist = 0)
twistedpris = Graph(vtxs, faces)
twist = 0

def setup():
    #noFill()
    size(1000, 1000)
    frame_rate=2

def draw():
    """global count
    global inc
    global t"""
    global twist


    background(120)
    no_fill()
    camera(4*(mouse_x-width/2), 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0)

    """if(count == 150):
        inc = 1/inc
        t = t*-1
        count = 0
    count += 1
    square.translate(t)"""
    twist += 0.005
    vtxs, faces = TwistedPrism(sides = 20, twist = twist)
    twistedpris = Graph(vtxs, faces)


    push()
    stroke(120, 0, 0)
    #sphere(99)
    pop()

   
    push()
    begin_shape()
    stroke(0)
    stroke_weight(100)
    twistedpris.plotFromFaces(sf=100)
    end_shape()
    pop()

    push()
    stroke(255)
    begin_shape()
    twistedpris.plotSphericalFromFaces(100)
    end_shape()
    pop()
    
    push()
    no_stroke()
    fill(120, 128)
    plane(10000, 10000)
    pop()

if __name__ == '__main__':
    run(mode='P3D')


