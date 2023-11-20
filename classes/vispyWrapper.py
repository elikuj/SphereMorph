# functionality to make current data structures compatible with vispy

import sys
import os
import vispy.scene.visuals as vp
from vispy.visuals.filters import Alpha
import numpy as np
import scipy as sci
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from classes.graph import *
from classes.node import *


class VispyGraph(Graph):
    faces = np.array([])
    vertices = np.array([])
    edges = np.array([])
    graph = Graph([])
    
    # constructor
    def __init__(self, graph):
        self.graph = graph
        self.faces = graph.faces
        self.vertices = graph.points
        self.edges = []
        # contruct list of edges
        for face in self.faces:
            for i in range(len(face)):
                self.edges.append([self.vertices[face[i]], self.vertices[face[(i+1)%len(face)]]])
        self.edges = np.array(self.edges)  
                              
    def outline(self, color="red"):
        return vp.Line(pos = self.edges, width=3, color=color, connect='segments', method='gl')
        #Canvas.view.add(outline)
        #return vp.Line(pos = self.vertices, width=3, color='red', connect="strip", method='gl')
        
    def guts(self, color="blue", alpha=0.3):
        shapeGuts = vp.Mesh(self.vertices, self.faces)
        alphilter = Alpha(alpha = alpha)
        shapeGuts.attach(alphilter)
        return shapeGuts
    
    def sphericalOutline(self, r):
        spherical_faces = []
        for face in self.faces:
            points = []
            for i in range(len(face)):
                pt = self.vertices[face[i]]
                mag = la.norm(pt)
                pt = pt/mag*r
            
                next = self.vertices[face[(i+1)%len(face)]]
                mag2 = la.norm(next)
                next = next/mag2*r
        
                normal = np.cross(pt, next)
                normal = normal/np.linalg.norm(normal)
                theta = math.acos(np.dot(pt, next)/r**2)
                divs = (int)(np.linalg.norm(pt-next)/(3))
                toplot = pt
               
                for j in range(0, divs):
                    rotvec = R.from_rotvec(normal * theta/divs)
                    toplot = np.array(rotvec.apply(toplot))
                    #vertex(toplot[0], toplot[1], toplot[2])
                    
                    points.append(np.array(toplot))
                    
            points = vp.Line(pos=np.array(points), width=3, color='black', connect='strip', method='gl')
            spherical_faces.append(points)
        return spherical_faces
        
    def kernel(self):
        kernel_graph = self.graph.kernel()
        return VispyGraph(kernel_graph).guts()
    
