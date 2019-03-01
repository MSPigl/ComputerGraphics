#Chris Fall and Matt Pigliavento
import viz
from Zones import *

# set size (in pixels) and title of application window
viz.window.setSize( 640, 480 )
viz.window.setName( "Zone Test" )

# get graphics window
window = viz.MainWindow

# set background color of window to black 
viz.MainWindow.clearcolor( viz.WHITE ) 

# center viewpoint 
viz.eyeheight(0)

z = ZoneController()

# render the scene in the window
viz.go()