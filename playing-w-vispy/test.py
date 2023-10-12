import sys
import numpy as np

import vispy
from vispy import scene
from vispy.color import Color
canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)

# Set up a viewbox to display the cube with interactive arcball
view = canvas.central_widget.add_view()
view.bgcolor = '#efefef'
view.camera = 'turntable'
view.padding = 100

color = Color("#3f51b5")

arr = np.array([[150, 0, 243],
[ 150,       0,    -242.7051],
[-150,       0,     242.7051],
[-150,       0,    -242.7051],
[242.7051, 150,      0,   ],
[ 242.7051, -150,       0,   ],
[-242.7051,  150,       0,   ],
[-242.7051, -150,       0,   ],
[  0,    242.7051, 150,   ],
[   0,     242.7051, -150   ],
[   0,    -242.7051,  150   ],
[   0,    -242.7051, -150   ]])

cube = scene.visuals.Sphere(1, 30, 30, color=(0, 0, 1, 0.1), edge_color=(0.5, 0.5, 1, 0.1), parent=view.scene)
#icos = vispy.geometry.isosurface(arr)

if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()