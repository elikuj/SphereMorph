import numpy as np
import numpy.linalg as la
import scipy.spatial as spat
from scipy.spatial.transform import Rotation as R
from p5 import *
import networkx as nx
import copy

class Node:
    coordinates = ()
    adjacencies = []
    # adjacencies should be stored in cyclic order.

    def __init__(self, adj, coords):
        self.adjacencies = adj
        self.coordinates = coords #tuple([c for c in coords])

    # plot point
    def plot(self):
        vertex(self.coordinates[0], self.coordinates[1], self.coordinates[2])

    # get coordinates as a np.array
    def arr(self):
        return np.asarray(self.coordinates)

    def update(self, newcoords):
        self.coordinates = (newcoords[0], newcoords[1], newcoords[2])

    # plot projection of point on sphere of radius r
    def spherical(self, r):
        mag = la.norm(np.array(self.coordinates))
        vertex(self.coordinates[0]*r/mag, self.coordinates[1]*r/mag, self.coordinates[2]*r/mag)
        return np.asarray(self.coordinates)*r/mag

    # get spherical coordinates as a np.array
    def sphericalCoords(self, r):
        mag = la.norm(np.array(self.coordinates))
        return np.asarray(self.coordinates)*r/mag
   

class Graph:
    points = []
    edges = 0

    def __init__(self, points):
        self.points = points
        self.edges = 0
        for pt in points:
            self.edges += len(pt.adjacencies)
        self.edges = self.edges/2

    def plot(self):
        visited = set()
        stack = [(self.points[0], self.points[0].adjacencies[0])]
        #path = []
        #begin_shape()
        while stack:
            current, parent = stack.pop()
            if (current, parent) not in visited and (parent, current) not in visited:
                begin_shape()
                current.plot()
                parent.plot()
                end_shape()
                visited.add((current, parent))
                #path.append(current)
                for neighbor in current.adjacencies:
                    #if neighbor not in visited:
                    stack.append((current, neighbor))
                for neighbor in parent.adjacencies:
                    #if neighbor not in visited:
                    stack.append((parent, neighbor))
                    #elif neighbor is not parent:
                        # Cycle detected
                        #cycle_idx = path.index(neighbor)
                        #return path[cycle_idx:] + [neighbor]
        #end_shape()

    def plotSpherical(self, r):
        visited = set()
        stack = [(self.points[0], self.points[0].adjacencies[0])]
        path = []
        #begin_shape()
        while stack:
            current, parent = stack.pop()
            if (current, parent) not in visited and (parent, current) not in visited:
                begin_shape()
                first = current.spherical(r)
                if(parent != None):
                    first = current.sphericalCoords(r)
                    second = parent.sphericalCoords(r)
                    normal = np.cross(first, second)
                    normal = normal/np.linalg.norm(normal)
                    theta = math.acos(np.dot(first, second)/r**2)
                    divs = (int)(np.linalg.norm(current.arr()-parent.arr())/10)
                    toplot = first
                    for i in range(0, divs):
                        rotvec = R.from_rotvec(normal * theta/divs)
                        toplot = rotvec.apply(toplot)
                        vertex(toplot[0], toplot[1], toplot[2])
                #if (current, parent) not in visited and (parent, current) not in visited:
                visited.add((current, parent))
                for neighbor in current.adjacencies:
                    stack.append((neighbor, current))
            end_shape()

    def vecsAsMatrix(self):
        mat = np.ndarray((len(self.points), 3), float)
        for i in range(len(self.points)):
            mat[i][0] = self.points[i].coordinates[0]
            mat[i][1] = self.points[i].coordinates[1]
            mat[i][2] = self.points[i].coordinates[2]
        return mat

    def matToPoints(self, mat):
        for i, point in enumerate(self.points):
            self.points[i].coordinates = (mat[i][0], mat[i][1], mat[i][2])
        return self.points

    def getCoords(self):
        toreturn = []
        for point in self.points:
            toreturn.append(point.coordinates)
        return toreturn
       
    def transform(self, tmat):
        self.matToPoints(self.vecsAsMatrix()@tmat)

    def projectToPlane(self):
        temp = copy.deepcopy(self)
        for point in temp.points:
            if(point.coordinates[2] != 0):
                point.update(point.spherical(100)*300/point.spherical(100)[2])
        temp.plot()

    def contract(self, i1, i2):
        fst = self.points[i1].arr()
        sec = self.points[i2].arr()
        vec = np.array(fst-sec)
        vec = vec/np.linalg.norm(vec)
        self.points[i2].update(sec+vec)
        self.points[i1].update(fst-vec)

    def translate(self, translation):
        for pt in self.points:
            pt.update(pt.arr()+translation)
           
A = Node([], (200, 100, 0))       
B = Node([], (-200, 100, 0))       
C = Node([], (200, -100, 0))       
D = Node([], (-200, -100, 0))       
E = Node([], (0, 200, 100))
F = Node([], (0, -200, 100))
G = Node([], (0, 200, -100))
H = Node([], (0, -200, -100))
I = Node([], (100, 0, 200))
J = Node([], (100, 0, -200))
K = Node([], (-100, 0, 200))
L = Node([], (-100, 0, -200))

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
    no_stroke()
    fill(120, 128)
    plane(10000, 10000)
    pop()

if __name__ == '__main__':
    run(mode='P3D')
