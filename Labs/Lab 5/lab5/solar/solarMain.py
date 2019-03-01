# solarMain.py
#
# Driver for a solar system program

import viz
from Solar import *

# set size of application window 
viz.window.setSize( 600, 600)
viz.window.setName( "Solar System Simulation" )

# set properties of MainWindow
window = viz.MainWindow
window.ortho(-600,+600,-600,+600,-1,1)
window.clearcolor( viz.BLACK )

# do not translate view up to eye height
viz.eyeheight(0)

# turn mouse navigation off
viz.mouse.setOverride(viz.ON) 

Solar()

viz.go()