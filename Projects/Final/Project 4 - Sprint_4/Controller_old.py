#Chris Fall and Matt Pigliavento
import viz
import vizshape
import math

class Controller(viz.EventClass):
	
	def __init__(self):
		
		
		viz.EventClass.__init__(self)
				
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
		self.callback(viz.TIMER_EVENT, self.onTimer)
		#self.callback(viz.MOUSEDOWN_EVENT, self.onMouse)
		
		self.x = 0
		self.y = 0
		self.z = 0
		
		#self.rotate = 0
		
		self.pitch = 0
		self.roll = 0
		self.yaw = 0
		
		space = viz.add(viz.ENVIRONMENT_MAP,'Skybox/stars.jpg')
		skybox = viz.add('skydome.dlc')
		skybox.texture(space)
		
		self.model =  None
		self.xWing = viz.add('x-wing/x-wing.dae')
		self.tie = viz.add('tie/tie.dae')
		self.destroyer = viz.add('destroyer/[.dae]/republic assault ship.dae')
		print ("Destroyer is at {}".format(self.destroyer.getCenter()))
		self.destroyer.setScale(15, 15, 15)
		self.destroyer.setPosition(0, -50, 600)
		
		self.picking = True
		self.pickShip()
		
		self.starttimer(1,1/20, viz.FOREVER)
		
		self.callback(viz.MOUSEDOWN_EVENT, self.onClick)


	def onTimer(self,num):
		
		if(num == 1):
			self.z += 5
			self.moveShip()

	def onKeyDown(self, key):
		if not self.picking:
			if (key == viz.KEY_LEFT): # move viewer to the left
				self.x -= 5
			elif (key == viz.KEY_RIGHT): # move viewer to the right
				self.x += 5
			elif (key == viz.KEY_UP):
				self.z += 5
			elif (key == viz.KEY_DOWN): 
				self.z -= 5
			elif (key == "u"): # move viewer up
				self.y += .5
			elif (key == "d"): # move viewer down
				self.y -= .5
				
			print("[{}, {}, {}]".format(self.x, self.y, self.z))
			self.moveShip()
		
	def onClick(self, click):
		if self.picking:
			choice = viz.pick(info = True)
			if choice.valid:
				if choice.object.id == self.xWing.id:
					print("xwing")
					self.model = self.xWing
					self.tie.remove()
					
					self.z += 10
					self.picking = False
				elif choice.object.id == self.tie.id:
					print("tie")
					self.model = self.tie
					self.xWing.remove()
					
					self.z += 10
					self.picking = False
				self.moveShip()

	def pickShip(self):
		self.picking = True
		
		m = viz.Matrix()
		m.postAxisAngle(0, 1, 0, 180)
		m.postTrans(-5, 0, 25)
		self.xWing.setMatrix(m)
		
		m = viz.Matrix()
		m.postTrans(5, 0, 25)
		self.tie.setMatrix(m)
	
	def moveShip(self):
		view = viz.MainView
		mat = viz.Matrix()
		if self.model.id == self.tie.id:
			mat.postAxisAngle(0, 1, 0, 180)
		mat.postTrans(self.x, self.y, self.z)
		self.model.setMatrix(mat)
		
		self.setView()
		
		print ("Centered at {}".format(self.model.getCenter()))
		
	def setView(self):
		m = viz.Matrix()
		m.postAxisAngle(1, 0, 0, 10)
		m.postTrans(self.x, self.y + 3, self.z - 15)
		
		view = viz.MainView
		view.setMatrix(m)
		
#	def onMouse(self):
#		return