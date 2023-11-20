# NOT FUNCTIONAL -- just to look pretty in screenshot

import numpy as np
import numpy.linalg as la
import scipy.spatial as spat
from scipy.spatial.transform import Rotation as R
from scipy.spatial import ConvexHull
from p5 import *
import classes.node

class Graph:
    points = []     # 2d np array of Points -- coordinates of vertices
    faces = []      # 2d np array; each element has indices of points in a face in cyclic order

    # constructor
    def __init__(self, points, faces = []):
        self.points = np.array(points)
        self.faces = faces
        self.edges = len(points) + len(faces) - 2

    # plots 3d polyhedron in space
    def plot(self):
        visited = set()
        stack = [(self.points[0], self.points[0].adjacencies[0])]
        while stack:
            current, parent = stack.pop()
            if (current, parent) not in visited and (parent, current) not in visited:
                begin_shape()
                current.plot()
                parent.plot()
                end_shape()
                visited.add((current, parent))
                for neighbor in current.adjacencies:
                    stack.append((current, neighbor))
                for neighbor in parent.adjacencies:
                    stack.append((parent, neighbor))
        
    # plots projection of polyhedron on sphere of radius r
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
        
    #   Compute the kernel of the graph by dualizing the convex hull of the dual graph (scaled by sf)
    #   returns kernel as Graph type
    def kernel(self, sf: int) -> Graph:
        dual_points = []
        for face in self.faces:             # computing vertices of dual graph
            v1 = self.points[face[1]] - self.points[face[0]]
            v2 = self.points[face[2]] - self.points[face[1]] 
            normal = np.cross(v1, v2)
            d = np.dot(self.points[face[1]], normal)
            dual_points.append(sf*np.array([normal[0], normal[1], normal[2]])/d)
        
        hull = ConvexHull(dual_points)      # convex hull of dual
        
        kernel_points = []
        for face in hull.simplices:         # computing vertices of dual of dual of convex hull
            v1 = dual_points[face[1]] - dual_points[face[0]]
            v2 = dual_points[face[2]] - dual_points[face[1]] 
            normal = np.cross(v1, v2)
            d = np.dot(dual_points[face[0]], normal)
            kernel_points.append(sf*np.array([normal[0], normal[1], normal[2]])/d)
        
        # convex hull of dual of convex hull of dual
        # convoluted but only works this way, for some reason
        kernel_hull = ConvexHull(kernel_points)     
        kernel = Graph(kernel_points, kernel_hull.simplices)  
        
        return kernel    
        
    # apply any matrix transformation tmat (3x3 np array) to polyhedron   
    def transform(self, tmat: np.array):
        self.matToPoints(self.vecsAsMatrix()@tmat)

    # project graph onto plane ax + by + cz + d = 0
    def projectToPlane(self, a, b, c, d):
        temp = copy.deepcopy(self)
        for point in temp.points:
            if(point.coordinates[2] != 0):
                point.update(point.spherical(100)*300/point.spherical(100)[2])
        temp.plot()

    # contract points[i1] and points[i2] towards each other
    def contract(self, i1, i2):
        fst = self.points[i1].arr()
        sec = self.points[i2].arr()
        vec = np.array(fst)-np.array(sec)
        vec = vec/np.linalg.norm(vec)
        self.points[i2].update(sec+vec)
        self.points[i1].update(fst-vec)

    # translate by translation vector amount
    def translate(self, translation: np.array):
        for pt in self.points:
            pt.update(pt.arr()+translation)
        
    # scale polyhedron by factor       
    def scale(self, factor):
        for point in self.points:
            point.coordinates = point.coordinates*factor
    
