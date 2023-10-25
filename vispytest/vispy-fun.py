import numpy as np
import sys
import os

from vispy import scene, app, geometry

from vispy.geometry.generation import create_sphere
from vispy.color.colormap import get_colormaps
 


vtxs = np.array([
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

fcs = np.array([
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


edges = []

for face in fcs:
    for i in range(len(face)):
        edges.append([vtxs[face[i]], vtxs[face[(i+1)%len(face)]]])

try:
    from sip import setapi
    setapi("QVariant", 2)
    setapi("QString", 2)
except ImportError:
    pass

try:
    from PyQt4 import QtCore
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import (QMainWindow, QWidget, QLabel,
                             QSpinBox, QComboBox, QGridLayout, QVBoxLayout,
                             QSplitter)
except Exception:
    # To switch between PyQt5 and PySide2 bindings just change the from import
    from PyQt5 import QtCore
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel,
                                 QSpinBox, QComboBox, QGridLayout, QVBoxLayout,
                                 QSplitter)

# Provide automatic signal function selection for PyQtX/PySide2
pyqtsignal = QtCore.pyqtSignal if hasattr(QtCore, 'pyqtSignal') else QtCore.Signal


class ObjectWidget(QWidget):
    """
    Widget for editing OBJECT parameters
    """
    signal_object_changed = pyqtsignal(name='objectChanged')

    def __init__(self, parent=None):
        super(ObjectWidget, self).__init__(parent)

        l_nbr_steps = QLabel("Nbr Steps ")
        self.nbr_steps = QSpinBox()
        self.nbr_steps.setMinimum(3)
        self.nbr_steps.setMaximum(100)
        self.nbr_steps.setValue(6)
        self.nbr_steps.valueChanged.connect(self.update_param)

        l_cmap = QLabel("Cmap ")
        self.cmap = sorted(get_colormaps().keys())
        self.combo = QComboBox(self)
        self.combo.addItems(self.cmap)
        self.combo.currentIndexChanged.connect(self.update_param)

        gbox = QGridLayout()
        gbox.addWidget(l_cmap, 0, 0)
        gbox.addWidget(self.combo, 0, 1)
        gbox.addWidget(l_nbr_steps, 1, 0)
        gbox.addWidget(self.nbr_steps, 1, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(gbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def update_param(self, option):
        self.signal_object_changed.emit()


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.resize(700, 500)
        self.setWindowTitle('vispy example ...')

        splitter = QSplitter(Qt.Horizontal)

        self.canvas = Canvas()
        self.canvas.create_native()
        self.canvas.native.setParent(self)

        self.props = ObjectWidget()
        splitter.addWidget(self.props)
        splitter.addWidget(self.canvas.native)

        self.setCentralWidget(splitter)
        self.props.signal_object_changed.connect(self.update_view)
        self.update_view()

    def update_view(self):
        # banded, nbr_steps, cmap
        self.canvas.set_data(self.props.nbr_steps.value(),
                             self.props.combo.currentText())


class Canvas(scene.SceneCanvas):

    def __init__(self):
        scene.SceneCanvas.__init__(self, keys=None)
        self.size = 800, 600
        self.unfreeze()
        self.view = self.central_widget.add_view()
        self.radius = 2.0
        self.view.camera = 'turntable'
        mesh = create_sphere(20, 20, radius=self.radius)
        vertices = mesh.get_vertices()
        tris = mesh.get_faces()

        cl = np.linspace(-self.radius, self.radius, 6 + 2)[1:-1]

        self.iso = scene.visuals.Isoline(vertices=vertices, tris=tris,
                                         data=vertices[:, 2],
                                         levels=cl, color_lev='autumn',
                                         parent=self.view.scene)
        self.freeze()

        # Add a 3D axis to keep us oriented
        scene.visuals.XYZAxis(parent=self.view.scene)
        #scene.visuals.Sphere(parent=self.view.scene)
        scene.visuals.Mesh(vertices=vtxs, faces=fcs, parent=self.view.scene)
        # self.view.add(poly)
        self.show()
        
        

    def set_data(self, n_levels, cmap):
        self.iso.set_color(cmap)
        cl = np.linspace(-self.radius, self.radius, n_levels + 2)[1:-1]
        self.iso.levels = cl


if __name__ == '__main__':
    app.create()
    win = MainWindow()
    win.show()
    app.run()
