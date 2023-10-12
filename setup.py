import numpy as np
import numpy.linalg as la
import scipy.spatial as spat
from scipy.spatial.transform import Rotation as R
from p5 import *
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

    # update coordinates
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
        
    def soften(self):
        for point in self.points:
            
            toadd = np.array([0,0,0])
            for p in point.adjacencies:
                toadd += p.coordinates
            toadd = toadd/len(point.adjacencies)
            point = 0.1*toadd + 0.9*point.adjacencies
                
            