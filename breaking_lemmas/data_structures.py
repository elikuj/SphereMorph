#   11/19/23: currently returns NO counterexamples!!! see notes.

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

def to_str(nparr):
    print("[")
    for i in range(3):
        print(f"[{nparr[i][0]}, {nparr[i][1]}, {nparr[i][2]}],")
    print("]")

# print(la.det(np.array([a,b,c])))
# print(la.det(np.array([a,b,-1*c])))


# helper functions
def random_northern_vertex():
    theta = random.random()*math.pi/4 + np.pi/4
    phi = random.random()*math.pi       # if phi \in [0, 2pi), we can obtain bad examples. constraining max(phi) = pi results in 100%(?) success rate.
    return (theta, phi)

def random_southern_vertex():
    theta = -1*random.random()*math.pi/4 - np.pi/4
    phi = random.random()*math.pi       # if phi \in [0, 2pi), we can obtain bad examples. constraining max(phi) = pi results in 100%(?) success rate.
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


#def get_bounds_on_c(a,b):
def constrain_c(a, b, N=np.array([0,0,1]), O=np.array([0,0,0])):
    uhh_plane = np.cross(O-a, O-b)
    c = random_southern_vertex()
    while np.dot(coords(c), uhh_plane)*np.dot(N, uhh_plane) >= 0:
        c = random_southern_vertex()
    return c

    


# compute determininant of original triangle abc and its fixed-latitude analog; check if signs are different
def test_dets(a, b, c):
    # det of original triangle:
    og_tri = np.array([coords(a), coords(b), coords(c)])
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
        to_str(np.array([coords(a),coords(b),coords(c)]))
        to_str(np.array([fixed_a, fixed_b, fixed_c]))
        return True
    else:
        print("❌ SELF INTERSECTION!!! ❌")
        #print(np.array([coords(a),coords(b),c]))
        #to_str(np.array([coords(a),coords(b),coords(c)]))
        #to_str(np.array([fixed_a, fixed_b, fixed_c]))
        return False
        
        
# run "trials" num of simulations.
# has yet to produce a counterexample in current version of simulation (as of 11/20/23)
def simulate(trials):
    fails = 0
    for i in range(trials):
        a = random_northern_vertex()
        b = random_northern_vertex()
        c = constrain_c(coords(a), coords(b))
        if not test_dets(a,b,c):
            fails += 1
    return fails

#print(simulate(10000))
    
