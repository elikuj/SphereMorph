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

class p5graph(Graph):
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
        
    # new_graph should be isomorphic to original graph
    def morph(self, new_graph, trans_factor=0.05):
        trans_vecs = self.points - new_graph.points
        for i, point in enumerate(self.points):
            point = trans_vecs[i]*trans_factor + point
            
        
        