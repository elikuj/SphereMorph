import numpy as np
import numpy.linalg as la
import numpy.random as rand
import scipy.spatial as spat
from scipy.spatial.transform import Rotation as R
from p5 import *
import classes.node
import classes.graph

class Kernel:
    parent = Graph(Point((0,0,0)))
    
    def __init__(polyhedron):
        self.parent = polyhedron
        kernel = AABB(polyhedron)
        
    
    
    
    def AABB(self):
        maxcorner = Point(self.parent.points[0])
        mincorner = Point(self.parent.points[1])
        # finding boundaries
        for point in self.parent.points:
            for i in range(3):
                mincorner[i] = min(points[i], mincorner[i])
                maxcorner[i] = min(points[i], maxcorner[i])
        
        # go through permutations of corresponding coordinates in mincorner and maxcorner + create graph object
    
    
        
        def phPlaneIntersection(self, kernel_face):
            for face in self.faces:
                
            