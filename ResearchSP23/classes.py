import numpy as np
import numpy.linalg as la
import scipy.spatial as spat
from p5 import *
import networkx as nx

class Node:
    adjacencies = []
    coordinates = ()

    def __init__(self, adj, coords):
        self.adjacencies = adj
        #self.coordinates = coords
        self.coordinates = tuple([100 * c for c in coords])

    def spherical(self, r):
        mag = la.norm(np.array(self.coordinates))
        vertex(self.coordinates[0]*r/mag, self.coordinates[1]*r/mag, self.coordinates[2]*r/mag)
    
    def plot(self):
        vertex(self.coordinates[0], self.coordinates[1], self.coordinates[2])

    

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

    
    #def plotSpherical(self, r):




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

def setup():
    #noFill()
    size(1000, 1000)

def draw():
    background(120)
    no_fill()
    camera(4*(mouse_x-width/2), 4*mouse_y, (height/2.0)/(math.tan(PI/6)), 0, 0, 0, 0, 1, 0)
    begin_shape()
    grap.plot()
    end_shape()

if __name__ == '__main__':
    run(mode='P3D')



G = nx.Graph()
for node in [A, B, C, D, E, F, G, H, I, J, K, L, M]:
    G.add_node(node)
    for neighbor in node.adjacencies:
        G.add_edge(node, neighbor)
print(nx.is_planar(G))
print(nx.node_connectivity(G))
