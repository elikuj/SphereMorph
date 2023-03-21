from p5 import *
import numpy as np


from scipy.spatial.transform import Rotation as R

"""import numpy as np
from scipy.ndimage.interpolation import rotate

x = np.random.randint(800, 1000, size=[100, 100, 3])
rotated = rotate(x, angle=45)"""

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

def plotShape(shape):
    begin_shape()
    for vtx in shape:
        vertex(vtx[0], vtx[1], vtx[2])
    end_shape()

def projectToSphere(shape, radius):
    begin_shape()
    for i, pt in enumerate(shape):
        first = np.array(pt)
        dif = np.array(shape[(i+1)%len(shape)]) - first
        for j in range(0, 21):
            toplot = ((first + dif*j/20))
            toplot = toplot * radius/np.linalg.norm(toplot)    
            vertex(toplot[0], toplot[1], toplot[2])
    end_shape()

# projects shape to sphere w/ given radius
# keeps distribution of points on sphere more equal
def projectByAngle(shape, radius):
    begin_shape()
    for i, pt in enumerate(shape):
        first_proj = np.array(pt)/(np.linalg.norm(pt))*radius
        next_proj = np.array(shape[(i+1)%len(shape)])/(np.linalg.norm(shape[(i+1)%len(shape)]))*radius
        normal = np.cross(first_proj, next_proj)
        normal = normal/np.linalg.norm(normal)
        theta = 2*math.acos(np.dot(first_proj, next_proj)/radius**2)
        divs = (int)(np.linalg.norm(np.array(pt) - np.array(shape[(i+1)%len(shape)]))/10)
        toplot = first_proj
        print("START")
        for i in range(0, divs):
            rotvec = R.from_rotvec(normal * theta/divs)
            toplot = rotvec.apply(toplot)
            print(f"[ {toplot[0]}, {toplot[1]}, {toplot[2]}],")
            vertex(toplot[0], toplot[1], toplot[2])
    end_shape()

def addVertex(vertex, shape, connectionidxs):
    # vertex: list with len=3
    # shape: 2D list
    # connectionidxs: list
    for i in range(len(connectionidxs)-1, -1, -1):
        cur = connectionidxs[i]
        shape.insert(cur+1, vertex)
        shape.insert(cur+2, shape[cur])


    return shape

# function for testing user input
def change(shape):
    shape = addVertex([200, 200, 200], shape, [0, 1, 4])
    plotShape(shape)
    
def stretch(shape, factor: float, dir: int):
    # dir = 0, 1, or 2
    cop = shape.copy()
    for vtx in cop:
        vtx[dir] = vtx[dir] * factor
    return cop

def setup():
    #noFill()
    size(1000, 1000)
    
    #lights()
    #directional_light(128, 128, 200, 0, 0, -1)
    
    
#stretchedoct = stretch(octahedron.copy(), 2, 0)


def draw():
    
    background(120)
    lights()
    ambient_light(100, 0, 0)
    
    camera(4*(mouse_x-width/2), 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0) #BEST
    #pointLight(51, 102, 126, 80, 20, 40)
    #adding vertex [200, 200, 200]
    #newoct = addVertex([200, 200, 200], octahedron, [0, 1, 4])

    #add shape
    plotShape(octahedron)
    projectToSphere(octahedron, 100)
    

    
    """plotShape(stretchedoct)
    projectToSphere(stretchedoct, 100)"""

    if key_is_pressed and key == '0':
        change(octahedron)
    
    if key_is_pressed and key == '1':
        oct = stretch(octahedron, 1.2, 0)
        plotShape(oct)
        projectToSphere(oct, 100)
        #projectByAngle(oct, 100)

    if key_is_pressed and key == '2':
        oct = stretch(octahedron, 1.2, 0)
        plotShape(oct)
        #projectToSphere(oct, 100)
        projectByAngle(oct, 100)
        
    
# subdision on actual sphere based on angle of curve 
# 
    

    

if __name__ == '__main__':
    run(mode='P3D')
