import numpy as np
import numpy.linalg as la
import scipy.spatial as spat
from scipy.spatial.transform import Rotation as R
from scipy.spatial import ConvexHull
from p5 import *
import classes.node

class Graph:
    points = []     # 2d np array of Points 
    faces = []      # 2d np array; each element has indices of points in a face of polyhedron in cyclic order
    edges = 0       # number of edges in polyhedron

    def __init__(self, points, faces = []):
        self.points = np.array(points)
        self.faces = faces
        self.edges = len(points) + len(faces) - 2

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
        
    def plotFromFaces(self, sf=1):
        for face in self.faces:
            begin_shape()
            for ptidx in face:
                pt = self.points[ptidx] *sf
                vertex(pt[0], pt[1], pt[2])
            end_shape()
                

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
            
    def plotSphericalFromFaces(self, r):
        for face in self.faces:
            begin_shape()
            for i in range(len(face)):
                pt = self.points[face[i]]
                mag = la.norm(pt)
                pt = pt/mag*r
            
                next = self.points[face[(i+1)%len(face)]]
                mag2 = la.norm(next)
                next = next/mag2*r
        
                normal = np.cross(pt, next)
                normal = normal/np.linalg.norm(normal)
                theta = math.acos(np.dot(pt, next)/r**2)
                divs = (int)(np.linalg.norm(pt-next)/10)
                toplot = pt
               
                for i in range(0, divs):
                    rotvec = R.from_rotvec(normal * theta/divs)
                    toplot = rotvec.apply(toplot)
                    vertex(toplot[0], toplot[1], toplot[2])
                
                #vertex(pt[0], pt[1], pt[2])
            end_shape(CLOSE)

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
        vec = np.array(fst)-np.array(sec)
        vec = vec/np.linalg.norm(vec)
        self.points[i2].update(sec+vec)
        self.points[i1].update(fst-vec)

    def translate(self, translation):
        for pt in self.points:
            pt.update(pt.arr()+translation)
        
            
    def scale(self, factor):
        for point in self.points:
            point.coordinates = point.coordinates*factor
            
    #   Compute the kernel of the graph by dualizing the convex hull of the dual graph
    #   returns kernel as Graph type
    def kernel(self, sf=1):
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
    
    def soften(self):
        for point in self.points:
            
            toadd = np.array([0.0,0.0,0.0])
            for p in point.adjacencies:
                toadd += p.arr()
            toadd = toadd*1.0/len(point.adjacencies)
            point.update(0.1*toadd + 0.9*point.arr())
            
    def morph(self, new_graph, trans_factor=0.05):
        trans_vecs = -1*(self.points - new_graph.points)
        for i, point in enumerate(self.points):
            point = trans_vecs[i]*trans_factor + point
            self.points[i]=point
        return self