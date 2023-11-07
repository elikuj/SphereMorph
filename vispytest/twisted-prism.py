# most successful vispy testing as of 10/16/23
# compatible with polyparser, all adapted methods from regular graph class are in vispyWrapper.py

import numpy as np
from vispy import scene
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.Qt import QVBoxLayout
from vispy.scene.visuals import Markers, Line, Mesh
from vispy.visuals.filters import ShadingFilter, WireframeFilter, Alpha

import sys
import os
# import local files
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from classes.graph import *
from classes.vispyWrapper import *
from classes.node import *

from polyparser import *


def TwistedPrism(sides=3, twist=1 / 12, height=2, radius=1):
    if twist > 1 / 2 - 1 / sides:
        print("❌DANGER❌ Self-intersecting twisted prism!")

    theta = np.linspace(0, 2 * np.pi, sides + 1)
    xbot = radius * np.cos(theta)
    ybot = radius * np.sin(theta)
    zbot = -height / 2
    xtop = radius * np.cos(theta - 2 * np.pi * twist)
    ytop = radius * np.sin(theta - 2 * np.pi * twist)
    ztop = height / 2

    botverts = [[xbot[i], ybot[i], zbot] for i in range(sides)]
    topverts = [[xtop[i], ytop[i], ztop] for i in range(sides)]
    vertices = np.array(botverts + topverts + [[0, 0, zbot], [0, 0, ztop]])

    botfaces = [[(i + 1) % sides, i, 2 * sides] for i in range(sides)]
    upfaces = [[i, (i + 1) % sides, sides + i] for i in range(sides)]
    dnfaces = [
        [(i + 1) % sides, sides + (i + 1) % sides, sides + i] for i in range(sides)
    ]
    topfaces = [
        [sides + i, sides + (i + 1) % sides, 2 * sides + 1] for i in range(sides)
    ]
    faces = np.array(botfaces + upfaces + dnfaces + topfaces)

    #SanityCheck(vertices, faces)  # ignore return value for now
    return (vertices, faces)
        
verts, faces = TwistedPrism(6, 0, 200, 100)
parsedpoly = VispyGraph(Graph(verts, faces))







class Canvas(scene.SceneCanvas):

    def __init__(self):
        scene.SceneCanvas.__init__(self, bgcolor='white', size=(800,800))
        
        self.unfreeze()
        self.view = self.central_widget.add_view()
        self.view.camera = 'turntable'
        #print('<__init__ canvas> scale_factor =', self.view.camera.scale_factor)
        #print('<__init__ canvas> center       =', self.view.camera.center)
        #print('<__init__ canvas> app          =', self.app)
        self.view.camera.scale_factor = 3

        
        
        """self.scatter = Markers()
        self.scatter.set_data(verts, edge_color='blue', face_color='red', 
                              edge_width=3, size=3)"""
       
        
        
        #self.view.add(self.scatter)
        
        #poly = Mesh(verts, faces)
        #self.view.add(poly)
        #wireframe_filter = WireframeFilter()
        alphilter = Alpha(alpha = 0.8)
        #shader = ShadingFilter()
        #scene.visuals.Sphere(parent=self.view.scene, radius = 80)
        #poly.attach(alphilter)
        #poly.attach(wireframe_filter)
        #poly.attach(shader)
        
        # self.view.add(parsedpoly.outline(color="black"))
        # self.view.add(parsedpoly.kernel())
        
        r=40
        vgraph_spherical = parsedpoly.sphericalOutline(r)
        for face in vgraph_spherical:
            self.view.add(face)
        
        sphere = scene.visuals.Sphere(radius=r)
        sphere.attach(alphilter)
        self.view.add(sphere)
        
        #self.view.add(parsedpoly.kernel(alpha=0.8))
        #self.view.add(parsedpoly.outline())

        self.freeze()
        
        
class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.resize(800, 800)
        self.setWindowTitle('SPHEREMORPH: VISUALIZED')

        vbox = QVBoxLayout()

        self.canvas = Canvas()
        self.canvas.create_native()
        self.canvas.native.setParent(self)

        vbox.addWidget(self.canvas.native)
        

if __name__ == '__main__':
    appQt = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    appQt.exec_()