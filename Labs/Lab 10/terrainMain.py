import viz
from TerrainController import *

# set size (in pixels) and title of application window
viz.window.setSize( 640*2, 480*2 )
viz.window.setName( "Terrain Lighting & Navigation" )

# get graphics window
window = viz.MainWindow
# set background color of window to black 
viz.MainWindow.clearcolor( viz.BLACK ) 
# turn off mouse navigation 
viz.mouse(viz.OFF)
# center viewpoint 
viz.eyeheight(0)

c = TerrainController()

# render the scene in the window
viz.go()