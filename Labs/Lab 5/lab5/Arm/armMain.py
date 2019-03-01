import viz
from Arm import *


# set size of application window 
viz.window.setSize( 600, 600)
viz.window.setName( "Robot Arm Simulation" )

# set properties of MainWindow
window = viz.MainWindow
window.ortho(-100,+100,-100,+100,-1,1)
window.clearcolor( viz.BLACK )

# do not translate view up to eye height
viz.eyeheight(0)

# turn mouse navigation off
viz.mouse.setOverride(viz.ON) 

Arm()

viz.go()