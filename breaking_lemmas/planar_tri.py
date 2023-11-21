# generate star-shaped planar triangulation:
import numpy as np
import numpy.linalg as la
import scipy as sci
from scipy.spatial import ConvexHull
import random
import matplotlib.pyplot as plt

#random.seed(1)

class star_shaped_planar_trianglation():
    points = []
    adjacencies = np.array([])
    boundary = np.array([])
    origin = np.array([0,0,0])
    n = 0   # num boundary points
    r = 1   # max radius
    
    
    def __init__(self, boundary=[], n=-1, r=1, k=-1):
        self.n = n
        self.k = k
        self.r = r
        if boundary == []:       # randomize EVERYTHING
            self.gen_boundary()
        else:
            self.boundary=boundary
        #     lalaa
        # else:
        #     n = len(boundary)
        if k != -1:
            self.gen_interior_points(k)
        #self.gen_boundary()
        #self.plot()
    
    def gen_boundary(self, lb=0.5):
        self.boundary = []
        for i in range(0, self.n):
            self.boundary.append([max(random.random()*self.r, self.r*lb), random.random()*np.pi*2])
        self.boundary = np.array(self.boundary)
        #print(self.boundary)
        self.boundary = self.boundary[self.boundary[:,-1].argsort()]     # sort by theta coord
        
            
            
    # plot the planar embedding. 
    # hopefully can be made compatible with many frontends, but currently support is only enabled for matplotlib.
    def plot(self, framework="matplotlib"):
        #if framework == "p5":
        
        #elif framework == "matplotlib":
        start_and_end = np.array([self.boundary[0], self.boundary[-1]]).T
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.set_rmax(self.r)
        ax.plot(start_and_end[1], start_and_end[0], color="orange")
        ax.plot(self.boundary.T[1], self.boundary.T[0], "orange")
        ax.set_title("Boundary of Gamma", va='bottom')
        
        for point in self.points:
            ax.plot(point[1], point[0], "bo--")
        plt.show()
        
        
        #elif framework == "vispy":
        
    '''def get_kernel(self):
        dual_points = []
        for point in self.boundary:
            return 3'''
            
    # test if given point lies within boundary of graph
    #def is_in_poly(self):
    
    
    # generate k interior points. 
    # currently runs in O(kn); could be optimized to O(logn*k) with binary search
    def gen_interior_points(self, k):
        for l in range(k):
            
            theta = random.random()*2*np.pi
            
            # find the 2 points on the boundary that theta lies in between
            i = 0
            while i < self.n and self.boundary[i][1] < theta:
                i+=1
            
            # find maximum r value for new point to keep it within the boundary of the embedding
            ax, ay = cartesian(self.boundary[(i-1)%self.n])
            bx, by = cartesian(self.boundary[(i)%self.n])
            t = (ax*np.tan(theta))/(by-ay-bx*np.tan(theta)+ax*np.tan(theta))-ay/(by-ay-bx*np.tan(theta)+ax*np.tan(theta))
            maxr = np.sqrt(((bx-ax)*t+ax)**2 + ((by-ay)*t+ay)**2)
            
            # append new point to array of interior points
            # constrain new point's radius so that it isn't super close to the boundary
            self.points.append([min(maxr*random.random(), maxr*0.9), theta])
        
    
            
def cartesian(polarpt):  # polarpt in form (r, theta)
    return polarpt[0]*np.cos(polarpt[1]), polarpt[0]*np.sin(polarpt[1])
            
        

      
i = star_shaped_planar_trianglation(n=20, k=20)
i.plot()