# Solar.py
#
# Simulates a solar system using a hierarchical model.

import viz
from solarUtil import *

class Solar( viz.EventClass):
	
	def __init__(self):
		viz.EventClass.__init__(self)
		
		# Call the addCircle function in solarUtil.py to initialize
		# these variables to circle layers
		self.sun = addCircle(50, viz.YELLOW)
		self.moon = addCircle(5, viz.WHITE)
		self.earth = addCircle(20, viz.GREEN)
		self.mercury = addCircle(5, viz.BLUE)
		
		# distances between orbs
		self.distMercurySun = 100
		self.distEarthSun = 400
		self.distMoonEarth = 45
		
		# location of the sun in the world coordinate system
		self.sunX = 0
		self.sunY = 0
		
		# current day of the simulation
		self.day = 0
		
		self.earth.setParent(self.sun)
		self.mercury.setParent(self.sun)
		self.moon.setParent(self.earth)
		
		self.setTransformations()
		
		self.callback(viz.TIMER_EVENT, self.onTimer)
		self.callback(viz.KEYDOWN_EVENT, self.onKeyDown)
		
		self.starttimer(1, 1/10, viz.FOREVER)
		
	# sets the transformation matices of the nodes in the scene graph	
	def setTransformations(self):
		m = viz.Matrix()
		m.postTrans(100, 0)
		m.postAxisAngle(0, 0, 1, (self.day/224.0) * 360)
		self.mercury.setMatrix(m)
		
		m = viz.Matrix()
		m.postTrans(400, 0)
		m.postAxisAngle(0, 0, 1, (self.day/365.0) * 360)
		self.earth.setMatrix(m)
		
		m = viz.Matrix()
		m.postTrans(45, 0)
		m.postAxisAngle(0, 0, 1, (self.day/30.0) * 360)
		self.moon.setMatrix(m)
		
	def onTimer(self, num):
		self.day += 1
		self.setTransformations()
	
	def onKeyDown(self, key):
		if key == viz.KEY_UP:
			self.sunY += 5
		elif key == viz.KEY_DOWN:
			self.sunY -= 5
		elif key == viz.KEY_RIGHT:
			self.sunX += 5
		elif key == viz.KEY_LEFT:
			self.sunX -= 5

		m = viz.Matrix()
		m.postTrans(self.sunX, self.sunY)
		self.sun.setMatrix(m)
			
		
	
		
		