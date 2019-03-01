#Chris Fall and Matt Pigliavento
import viz
from Controller import *

# set size (in pixels) and title of application window
viz.window.setSize( 640*4, 480*4 )
viz.window.setName( "Trench-Run - Final" )

# get graphics window
window = viz.MainWindow

# set background color of window to black 
viz.MainWindow.clearcolor( viz.BLACK ) 
# turn off mouse navigation 
viz.mouse(viz.OFF)
# center viewpoint 
viz.eyeheight(0)

viz.phys.enable()

c = Controller()

# render the scene in the window
viz.go()
