# Matt Pigliavento
# Siena College, Fall 2017
# main.py

import viz

from Coaster import *

# set size (in pixels) and title of application window
viz.window.setSize( 500, 500 )
viz.window.setName( "Coaster" )

# get graphics window
window = viz.MainWindow
# setup viewing volume
window.ortho(-200,200,-200,200,-200,200)
# set background color of window to very light gray 
viz.MainWindow.clearcolor( [150,150,150] ) 
# center viewpoint 
viz.eyeheight(0)

c = Coaster()

# render the scene in the window
viz.go()