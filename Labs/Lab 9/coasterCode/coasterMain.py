
# This is the driver for the coaster lab

import math
import viz
import vizcam
from CoasterController import *

# set size (in pixels) and title of application window
viz.window.setSize( 900, 900 )
viz.window.setName( "The Cobra Coaster" )

# get graphics window
window = viz.MainWindow

# set background color of window to black 
viz.MainWindow.clearcolor( viz.BLACK ) 

c = CoasterController()

# render the scene in the window
viz.go()