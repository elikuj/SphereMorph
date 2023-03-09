from p5 import *
import numpy as np

octahedron = [
    [200, 0, 0],
    [0, 0, 200],
    [-200, 0, 0],
    [0, 0, -200],
    [0, 200, 0],
    [0, 0, 200],
    [0, -200, 0],
    [0, 0, -200],
    [200, 0, 0],
    
    [0, 200, 0],
    [-200, 0, 0],
    [0, -200, 0],
    [200, 0, 0]
]

def projectToSphere(shape, radius):
    begin_shape()
    for i, pt in enumerate(shape):
        first = np.array(pt)
        dif = np.array(shape[(i+1)%len(shape)]) - first
        for j in range(0, 5):
            toplot = ((first + dif*j/4))
            toplot = toplot * radius/np.linalg.norm(toplot)
            if(j == 0 or j == 4):
                vertex(toplot[0], toplot[1], toplot[2])
                
            curve_vertex(toplot[0], toplot[1], toplot[2])
        vertex(300, 300, 0)


    end_shape()

def setup():
    size(1000, 1000)
    #translate(500, -500)
    
def draw():
    background(150)
    '''camera(-4*mouse_x, -4*mouse_y,(height/2) / tan(PI/6), width/2, height/2, 0, 0, 1, 0)
    camera(mouse_x, -mouse_y, 500 ,500, 500, 0, 0, 1, 0)'''
    #camera(4*mouse_x, 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0) #BEST
    #(height/2) / tan(PI/6)
    orbit_control()
    begin_shape()
    """for i in octahedron:
        vertex(i[0], i[1], i[2])
    end_shape()"""
    projectToSphere(octahedron, 200)
    

if __name__ == '__main__':
    run(mode='P3D')
