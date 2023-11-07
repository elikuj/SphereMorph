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

from classes.vispyWrapper import *
from classes.node import *

class Canvas(scene.SceneCanvas):

    def __init__(self):
        scene.SceneCanvas.__init__(self, bgcolor='white', size=(800,800))
        
        self.unfreeze()
        self.view = self.central_widget.add_view()
        self.view.camera = 'turntable'
        print('<__init__ canvas> scale_factor =', self.view.camera.scale_factor)
        print('<__init__ canvas> center       =', self.view.camera.center)
        print('<__init__ canvas> app          =', self.app)
        self.view.camera.scale_factor = 3

        verts = np.array([
            [50, 0, 81],
            [50, 0, -81],
            [-50, 0, 81],
            [-50, 0, -81],
            [81, 50, 0],
            [81, -50, 0],
            [-81, 50, 0],
            [-81, -50, 0],
            [0, 81, 50],
            [0, 81, -50],
            [0, -81, 50],
            [0, -81, -50]
        ])
        faces = np.array([
            [0, 2, 10],
            [0, 10, 5],
            [0, 5, 4],
            [0, 4, 8],
            [0, 8, 2],
            [3, 1, 11],
            [3, 11, 7],
            [3, 7, 6],
            [3, 6, 9],
            [3, 9, 1],
            [2, 6, 7],
            [2, 7, 10],
            [10, 7, 11],
            [10, 11, 5],
            [5, 11, 1],
            [5, 1, 4],
            [4, 1, 9],
            [4, 9, 8],
            [8, 9, 6],
            [8, 6, 2]
        ])
        
        lines = []

        for face in faces:
            for i in range(len(face)):
                lines.append(verts[face[i]])
                lines.append(verts[face[(i+1)%len(face)]])
                
        lines = np.array(lines)
        
        self.scatter = Markers()
        self.scatter.set_data(verts, edge_color='blue', face_color='red', 
                              edge_width=3, size=3)
       
        
        lines = Line(pos=lines, width=3, color='green', connect='segments', method='gl')
        self.view.add(lines)
        
        self.view.add(self.scatter)
        
        poly = Mesh(verts, faces)
        #self.view.add(poly)
        wireframe_filter = WireframeFilter()
        alphilter = Alpha(alpha = 0.3)
        #shader = ShadingFilter()
        scene.visuals.Sphere(parent=self.view.scene, radius = 80)
        poly.attach(alphilter)
        poly.attach(wireframe_filter)
        #poly.attach(shader)

        self.freeze()
        
        
class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.resize(800, 800)
        self.setWindowTitle('Visual test')

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