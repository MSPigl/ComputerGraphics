import viz

class Arm(viz.EventClass):
	
	def __init__(self):
		viz.EventClass.__init__(self)
		
		# create 3 layers here for base, upper arm, and lower arm
		# Base
		viz.startLayer(viz.POLYGON)
		viz.vertexColor(viz.RED)
		viz.vertex(-25, 10)
		viz.vertex(25, 10)
		viz.vertex(25, 0)
		viz.vertex(-25, 0)
		self.base = viz.endLayer()
		
		# UA
		viz.startLayer(viz.POLYGON)
		viz.vertexColor(viz.BLUE)
		viz.vertex(0, 5)
		viz.vertex(40, 5)
		viz.vertex(40, 0)
		viz.vertex(0, 0)
		self.upperArm = viz.endLayer()
		
		# LA
		viz.startLayer(viz.POLYGON)
		viz.vertexColor(viz.WHITE)
		viz.vertex(0, 5)
		viz.vertex(20, 5)
		viz.vertex(20, 0)
		viz.vertex(0, 0)
		self.lowerArm = viz.endLayer()
		
		# starting configuration
		self.ua = 120
		self.la = 85
		self.baseX = 0
		self.baseY = 0
				
		self.upperArm.setParent(self.base)
		self.lowerArm.setParent(self.upperArm)
		
		self.setTransformations()
		
		self.callback(viz.KEYDOWN_EVENT, self.onKeyDown)	
		
	def setTransformations(self):
		m = viz.Matrix()
		m.postTrans(self.baseX, self.baseY)
		self.base.setMatrix(m)
		
		m = viz.Matrix()
		m.postAxisAngle(0, 0, 1, self.ua)
		m.postTrans(0, 10)
		self.upperArm.setMatrix(m)
		
		m = viz.Matrix()
		m.postAxisAngle(0, 0, 1, self.la)
		m.postTrans(40, 0)
		self.lowerArm.setMatrix(m)
	
		
	def onKeyDown(self, key):
		if key == viz.KEY_LEFT:
			self.ua += 5
		elif key == viz.KEY_RIGHT:
			self.ua -= 5
		elif key == viz.KEY_UP:
			self.la -= 5
		elif key == viz.KEY_DOWN:
			self.la += 5
		elif key == 'a':
			self.baseX -= 5
		elif key == 'd':
			self.baseX += 5
		
		self.setTransformations()