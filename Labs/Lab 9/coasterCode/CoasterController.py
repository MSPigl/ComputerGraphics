# This is the controller class for the roller coaster simulation lab.
#

import viz
import vizmat
import vizshape
from CoasterCurve import *

class CoasterController(viz.EventClass):
	
	# constructor
	def __init__(self):
		
		viz.EventClass.__init__(self)

		# curve that represents the track
		self.track = CoasterCurve()
		
		# controls the camera's view in 3rd person
		self.rotateView = 0
		self.distView = -200
		self.view = 3
	
		# Environment map - puts the scene inside a large box and 
		# texture maps sky images onto the six box sides.
		sky = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
		skybox = viz.add('skydome.dlc')
		skybox.texture(sky)

		# Create a coaster car consisting of a box with a spherical cap in front.
		# The front of the car faces down the -Z axis.
		self.car = viz.addGroup()
		c1 = vizshape.addBox( [2,2,4], color = viz.GREEN)
		m = viz.Matrix()
		m.postTrans(0,1,0)  # raise bottom of box to XY plane
		c1.setMatrix(m)
		c1.setParent(self.car)
		c1 = vizshape.addBox( [1,2,1.9], color = viz.BLACK)
		m = viz.Matrix()
		m.postTrans(0,1.5,1)  
		c1.setMatrix(m)
		c1.setParent(self.car)
		c2 = vizshape.addSphere(radius=1, color = viz.YELLOW)
		m = viz.Matrix()
		m.postTrans(0,1,-2) # move to front of box
		c2.setMatrix(m)
		c2.setParent(self.car)
		
		viz.startLayer(viz.LINE_STRIP)
		viz.vertexColor(viz.BLACK)
		for i in range (1, 928):
			temp = self.track.getLocationAtDist(i)
			viz.vertex(temp)
		self.lineStrip = viz.endLayer()

		self.tunnel = vizshape.addCylinder(height = 75, radius = 10, bottom = False, top = False, cullFace = False)
		m = viz.Matrix()
		m.postAxisAngle(1,0,0,90)
		m.postMult(self.track.getCurOrient())
		m.postTrans(self.track.getCurLocation())
		m.postTrans(75,0,0)
		self.tunnel.setMatrix(m)
		
		
		self.tunnelText = viz.addTexture('tunnel.jpg')
		self.tunnel.texture(self.tunnelText)
			
		
		
		# set key board callback function
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
			
		# call keyboard callback to initialize the view to 3rd person
		self.onKeyDown( "3" )
	
	def onKeyDown(self,key):
		
		if key == 'r':
			self.track.resetTime()
		
		if key == 'a':
			self.track.advanceTime(.2)
		if key == 'd':
			self.track.advanceTime(-.2)

		if (key == "3"):
			self.view = 3
		elif (key == viz.KEY_LEFT):
			self.rotateView += 5
		elif (key == viz.KEY_RIGHT):
			self.rotateView -= 5
		elif (key == viz.KEY_UP):
			self.distView += 5
		elif (key == viz.KEY_DOWN):
			self.distView -= 5
			
		if (key == "1"):
			self.view = 1
		elif (key == viz.KEY_LEFT):
			self.rotateView += 1
		elif (key == viz.KEY_RIGHT):
			self.rotateView -= 1
			
		if (self.view == 1):
			# set camera view for 3rd person 
			view = viz.MainView
			m = viz.Matrix()
			m.postAxisAngle(0, 1, 0, 180)
			m.postTrans(0, 5, -5)
			m.postAxisAngle( 0,1,0, self.rotateView) 
			m.postMult(self.track.getCurOrient())
			m.postTrans(self.track.getCurLocation())
			view.setMatrix(m)
		
		if (self.view == 3):
			# set camera view for 3rd person 
			view = viz.MainView
			m = viz.Matrix()
			m.postTrans(0,0,self.distView) # move camera down -Z axis
			m.postAxisAngle( 0,1,0, self.rotateView)  # rotate about Y axis
			view.setMatrix(m)	
		
		m = viz.Matrix()
		m.postMult(self.track.getCurOrient())
		m.postTrans(self.track.getCurLocation())
		self.car.setMatrix(m)
		
			
					