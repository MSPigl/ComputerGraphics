# File: main.py

import viz
from Controller import *

# set size (in pixels) and title of application window
viz.window.setSize(500, 500)
viz.window.setName("BallZ")

# get graphics window
window = viz.MainWindow

# setup viewing rectangle
window.ortho(-100,100,-100,100,-1,1)

# set background color of window to black 
viz.MainWindow.clearcolor(viz.BLACK) 

# turn off mouse navigation 
viz.mouse(viz.OFF)

# center viewpoint 
viz.eyeheight(0)

# create a controller object
Controller()

viz.go()