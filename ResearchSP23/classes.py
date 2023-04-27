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
        self.coordinates = tuple([100 * c for c in coords])

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
        stack = [(self.points[0], None)]
        path = []
        begin_shape()
        while stack:
            current, parent = stack.pop()
            current.plot()
            if current not in visited:
                visited.add(current)
                path.append(current)
                for neighbor in current.adjacencies:
                    #if neighbor not in visited:
                    stack.append((neighbor, current))
                    #elif neighbor is not parent:
                        # Cycle detected
                        #cycle_idx = path.index(neighbor)
                        #return path[cycle_idx:] + [neighbor]
        end_shape()

    def plotSpherical(self, r):
        visited = set()
        stack = [(self.points[0], self.points[-1])]
        path = []
        #begin_shape()
        while stack:
            current, parent = stack.pop()
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
            if current not in visited:
                visited.add(current)
                path.append(current)
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


one = Node([], (3, 3, 0))
two = Node([], (3, -3, 0))
one.adjacencies = [two]
two.adjacencies = [one]
simple = Graph([one, two])

def stretchmat(factor):
    return np.array([[factor, 0, 0], [0, 1, 0], [0, 0, 1]])

count = 0
inc = 1.5


def setup():
    #noFill()
    size(1000, 1000)
    frame_rate=5

def draw():
    global count
    global inc

    background(120)
    no_fill()
    camera(4*(mouse_x-width/2), 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0)

    if(count == 10):
        inc = 1/inc
        count = 0

    count += 1
    

    begin_shape()
    grap.plot()
    end_shape()

    push()
    stroke(255)
    grap.plotSpherical(100)
    pop()

    push()
    stroke(255, 0, 0)
    grap.projectToPlane()
    pop()

if __name__ == '__main__':
    run(mode='P3D')

