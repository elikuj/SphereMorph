import numpy as np
import numpy.linalg as la
import math
import random


# ignore this
class sphericalEmbedding:
    longs = []
    lats = []
    origin = np.array([0,0,0])
    radius = 1
    adjacencies = []
    
    
    def __init__(self, lats, longs, adjacencies, radius=1, O=np.array([0,0,0])):
        self.lats = lats
        self.longs = longs
        self.origin = O
        self.radius = radius
        self.adjacencies = adjacencies
        
    def triVol(a, b, c):
        return la.det(np.array[a,b,c])
    
    
class planarEmbedding:
    vtxs = []
    
        

# a = np.array([math.sqrt(2),math.sqrt(2),0])
# b = np.array([-math.sqrt(2),math.sqrt(2),0])
# c = np.array([0,0,2])


# print(la.det(np.array([a,b,c])))
# print(la.det(np.array([a,b,-1*c])))


# helper functions
def random_northern_vertex():
    theta = random.random()*math.pi/2
    phi = random.random()*math.pi
    return (theta, phi)

def random_southern_vertex():
    theta = -1*random.random()*math.pi/2
    phi = random.random()*math.pi
    return (theta, phi)
    
def coords(vtx):
    theta = vtx[0]
    phi = vtx[1]
    return np.array([np.cos(theta)*np.cos(phi), np.cos(theta)*np.sin(phi), np.sin(theta)])

# fix latitude
def fix_north(vtx):
    phi = vtx[1]
    theta = np.pi/4
    return np.array([np.cos(theta)*np.cos(phi), np.cos(theta)*np.sin(phi), np.sin(theta)])

def fix_south(vtx):
    phi = vtx[1]
    theta = -1*np.pi/4
    return np.array([np.cos(theta)*np.cos(phi), np.cos(theta)*np.sin(phi), np.sin(theta)])


# compute determininant of original triangle abc and its fixed-latitude analog; check if signs are different
def test_dets(a, b, c):
    # det of original triangle:
    og_tri = np.array([a, b, c])
    fixed_a = fix_north(a)
    fixed_b = fix_north(b)
    fixed_c = fix_south(c)
    fixed_tri = np.array([fixed_a, fixed_b, fixed_c])
    og_det = la.det(og_tri)
    fixed_det = la.det(fixed_tri)
    #print(og_det)
    #print(fixed_det)
    if og_det*fixed_det >= 0:
        print("No self-intersection!")
        return True
    else:
        print("❌ SELF INTERSECTION!!! ❌")
        return False
        
        
# run "trials" num of simulations.
# currently returns "self intersection" about 50% of times, but there's probably something wrong with it
def simulate(trials):
    fails = 0
    for i in range(trials):
        a = coords(random_northern_vertex())
        b = coords(random_northern_vertex())
        c = coords(random_southern_vertex())
        if not test_dets(a, b, c):
            fails += 1
    return fails

print(simulate(100))
    
