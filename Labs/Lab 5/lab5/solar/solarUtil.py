# File solarUtil.py
#

import viz
import math


# Creates a layer consisting of a circular polygon whose radius (r)
# and color (color) are given as inputs.  It returns a reference to
# the layer (i.e. scene graph node).
def addCircle(r, color):
	viz.startLayer(viz.POLYGON)
	viz.vertexColor(color)
	for angle in range(0,360,10):
		viz.vertex(r*math.cos(math.radians(angle)), r*math.sin(math.radians(angle)))
	return viz.endLayer()	
	

		
	
		
		
		