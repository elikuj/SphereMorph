import numpy as np
import numpy.linalg as la
import scipy.spatial as spat
from scipy.spatial.transform import Rotation as R
from p5 import *
import copy


class Face:
    adjacencies = np.array([])
    normal = np.array([])
    
    def __init__(self, adjs):
        self.adjacencies = adjs
        v1 = adjs[1] - adjs[0]
        v2 = adjs[2] - adjs[1] 
        self.normal = np.cross(v2, v1)