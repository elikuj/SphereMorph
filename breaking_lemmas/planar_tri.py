# generate star-shaped planar triangulation

import numpy as np
import numpy.linalg as la
import scipy as sci
from scipy.spatial import ConvexHull, Delaunay
import random
import matplotlib.pyplot as plt
import triangle as tri

#random.seed(1)

class star_shaped_planar_trianglation():
    points = []
    adjacencies = np.array([])
    boundary = np.array([])
    origin = np.array([0,0,0])
    n = 0       # num boundary points
    r = 1       # max radius
    k = 0       # num interior points
    points_all_cart = []

    
    # ctor
    # n = num. points in boundary.
    # r = radius of bounding circle.
    # k = num. points in interior.
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
        self.points_all_cart = np.concatenate((self.boundary, self.points))
        #self.points_all_cart = cartesian([self.points_all_cart[:,0], self.points_all_cart[:,1]])
        for i, pt in enumerate(self.points_all_cart):
            self.points_all_cart[i] = cartesian(pt)
        #print(self.points_all_cart)
    
    # generate embedding's boundary.
    # generated in polar coordinates; sorts by theta coord so the boundary is ordered and star-shaped.
    # lb sets the lower bound for distance from origin, so each generated point is at least lb*r distance from o.
    def gen_boundary(self, lb=0.5):
        self.boundary = []
        for i in range(0, self.n):
            self.boundary.append([max(random.random()*self.r, self.r*lb), random.random()*np.pi*2])
        self.boundary = np.array(self.boundary)
        self.boundary = self.boundary[self.boundary[:,-1].argsort()]     # sort by theta coord
        

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


    def triangulate(self):
        return

    # plot the planar embedding.
    # uses polar coordinates.
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
    
    # triangulate and plot. final function for generating planar triangulation.
    def plot_triangulation(self):
        #print(self.points_all_cart)
        #tri = Delaunay(self.points_all_cart)
        #print(tri.simplices)
    
        # plt.triplot(self.points_all_cart[:,0], self.points_all_cart[:,1], tri.simplices.copy()) 
        # plt.plot(self.points_all_cart[:,0], self.points_all_cart[:,1], 'o')  
        # plt.plot(self.points_all_cart[0:self.n,0], self.points_all_cart[0:self.n,1], color="orange")
        
        #triangulation = tri.get_data({"vertices": self.points_all_cart})
        segments = []
        for i in range(self.n):
            segments.append([i, (i+1)%self.n])
            
        t = tri.triangulate({"vertices": self.points_all_cart,
                             "segments": segments}, "p")

        tri.compare(plt, {"vertices": self.points_all_cart,
                          "segments": segments}, t)


        print(t)
        plt.show()

            
    # writing graph to .poly file format, so it can use the triangle library for triangulations that preserve boundary        
    def write_poly_file(self, filename):
        f = open(filename, "a")
        f.write(f"{self.n+self.k}   2   0   1\n")
        for i, pt in enumerate(self.points_all_cart):
            if i < self.k:
                f.write(f"{i+1}   {pt[0]}   {pt[1]}     1\n")
            else:
                f.write(f"{i+1}   {pt[0]}   {pt[1]}\n")
        f.write(f"{self.n}  1\n")
        for i in range(self.n):
            f.write(f"{i+1}    {i+1}    {(i+1)%self.n+1}  1\n")
        f.close()
        
    
# helper f'n            
def cartesian(polarpt):  # polarpt in form (r, theta)
    return polarpt[0]*np.cos(polarpt[1]), polarpt[0]*np.sin(polarpt[1])
            
        

      
i = star_shaped_planar_trianglation(n=20, k=20)
#i.write_poly_file("pf.poly")
i.plot_triangulation()