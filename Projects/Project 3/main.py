# Matt Pigliavento
# Siena College, Fall 2017
# main.py

import viz
import vizfx

from TerrainGenerator import *

# set size (in pixels) and title of application window
viz.window.setSize( 640, 480 )
viz.window.setName( "Diamond-Square Terrain" )

# get graphics window
window = viz.MainWindow

# set background color of window to very light gray 
viz.MainWindow.clearcolor( [0,255,0] ) 
# center viewpoint 
viz.eyeheight(0)

t = TerrainGenerator()

# render the scene in the window
viz.go()