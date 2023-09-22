import numpy as np
import numpy.linalg as la
import scipy.spatial as spat
from scipy.spatial.transform import Rotation as R
from p5 import *
import copy

class Node:
    coordinates = []
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
        self.coordinates = np.array([newcoords[0], newcoords[1], newcoords[2]])

    # plot projection of point on sphere of radius r
    def spherical(self, r):
        mag = la.norm(self.coordinates)
        vertex(self.coordinates[0]*r/mag, self.coordinates[1]*r/mag, self.coordinates[2]*r/mag)
        return self.coordinates*r/mag

    # get spherical coordinates as a np.array
    def sphericalCoords(self, r):
        mag = la.norm(self.coordinates)
        return self.coordinates*r/mag
   

