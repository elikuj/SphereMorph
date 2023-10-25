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


from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel,
                                 QSpinBox, QComboBox, QGridLayout, QVBoxLayout,
                                 QSplitter, QSlider)

# Provide automatic signal function selection for PyQtX/PySide2
pyqtsignal = QtCore.pyqtSignal if hasattr(QtCore, 'pyqtSignal') else QtCore.Signal



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

twst = 0


verts, faces = TwistedPrism(sides = 12, twist = twst)
vgraph = VispyGraph(Graph(verts, faces))


class ObjectWidget(QWidget):
    """
    Widget for editing OBJECT parameters
    """
    signal_object_changed = pyqtsignal(name='objectChanged')
    twst = 0

    def __init__(self, parent=None):
        super(ObjectWidget, self).__init__(parent)
        
        l_twist = QLabel("Twist")
        self.twist_control = QSlider()
        self.twist_control.setMinimum(-1)
        self.twist_control.setMaximum(1)
        self.twist_control.setValue(0)
        self.twist_control.valueChanged.connect(self.update_param)

        # l_nbr_steps = QLabel("Nbr Steps ")
        # self.nbr_steps = QSpinBox()
        # self.nbr_steps.setMinimum(3)
        # self.nbr_steps.setMaximum(100)
        # self.nbr_steps.setValue(6)
        # self.nbr_steps.valueChanged.connect(self.update_param)

        # l_cmap = QLabel("Cmap ")
        # self.cmap = sorted(get_colormaps().keys())
        # self.combo = QComboBox(self)
        # self.combo.addItems(self.cmap)
        # self.combo.currentIndexChanged.connect(self.update_param)

        gbox = QGridLayout()
        #gbox.addWidget(l_cmap, 0, 0)
        #gbox.addWidget(self.combo, 0, 1)
        #gbox.addWidget(l_nbr_steps, 1, 0)
        #gbox.addWidget(self.nbr_steps, 1, 1)
        gbox.addWidget(self.twist_control)

        vbox = QVBoxLayout()
        vbox.addLayout(gbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def update_param(self, option):
        self.signal_object_changed.emit()




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
       
        verts, faces = TwistedPrism(sides = 12, twist = twst)
        self.vgraph = VispyGraph(Graph(verts, faces))
        
        #self.view.add(self.scatter)
        
        #poly = Mesh(verts, faces)
        #self.view.add(poly)
        #wireframe_filter = WireframeFilter()
        #alphilter = Alpha(alpha = 0.3)
        #shader = ShadingFilter()
        #scene.visuals.Sphere(parent=self.view.scene, radius = 80)
        #poly.attach(alphilter)
        #poly.attach(wireframe_filter)
        #poly.attach(shader)
        
        self.view.add(self.vgraph.outline())
        
        
        '''vgraph_spherical = parsedpoly.sphericalOutline(25)
        for face in vgraph_spherical:
            self.view.add(face)
            
        self.view.add(scene.visuals.Sphere(radius=25))'''
        
        self.view.add(self.vgraph.kernel())
        #self.view.add(parsedpoly.outline())
        
    def set_data(self, n_levels, cmap):
        global twst
        twst += 0.1
        #verts, faces = TwistedPrism(sides = 12, twist = twst)
        #self.vgraph = VispyGraph(Graph(verts, faces))
        
        #cl = np.linspace(-self.radius, self.radius, n_levels + 2)[1:-1]
        #self.iso.levels = cl
        
 
        
        
        
        
        
        
class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.resize(800, 800)
        self.setWindowTitle('SPHEREMORPH: VISUALIZED')

        vbox = QVBoxLayout()

        self.canvas = Canvas()
        self.canvas.create_native()
        self.canvas.native.setParent(self)

        
        splitter = QSplitter(Qt.Horizontal)

        
        self.props = ObjectWidget()
        splitter.addWidget(self.props)
        splitter.addWidget(self.canvas.native)

        self.setCentralWidget(splitter)
        self.props.signal_object_changed.connect(self.update_view())
        

        #self.freeze()
        
    def update_view(self):
        self.props.twst += 0.1
        self.canvas.set_data(self.props.twst)

        


if __name__ == '__main__':
    appQt = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    appQt.exec_()