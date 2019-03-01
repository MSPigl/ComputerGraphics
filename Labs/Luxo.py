# Luxo.py

import viz
import vizshape

class Luxo(viz.EventClass):

	# Constructor 
	def __init__(self):
		# must call constructor of EventClass first!!
		viz.EventClass.__init__(self)
		
		#Luxo instance variables that describe configuration
		self.x = 0    # location of base in world
		self.y = 0
		self.z = 0
		self.a = 30   # rotation angle of lower arm 
		self.b = 20   # spin angle of lower arm 
		self.c = -30  # rotation angle of upper arm 
		self.d = 0    # rotation angle of shade 
		self.e = 0    # spin angle of shade 
		
		self.animationCounter = 0
		
		self.base = vizshape.addCylinder(height = 5, radius = 20, axis = vizshape.AXIS_Y, slices = 20, bottom = True, top = True)
		
		m = viz.Matrix()
		m.postTrans(0,2.5,0)
		self.base.setMatrix(m)
		
		self.baseGroup = viz.addGroup()
		self.base.setParent(self.baseGroup)
		
		self.lowerArmGroup = viz.addGroup()
		self.lowerSphere = vizshape.addSphere(radius = 5, slices = 20, stacks = 20)
		self.lowerCyl = vizshape.addCylinder(height = 40, radius = 2.5, axis = vizshape.AXIS_Y, slices = 20, bottom = True, top = True)
		m = viz.Matrix()
		m.postTrans(0, 20, 0)
		self.lowerCyl.setMatrix(m)
		
		self.lowerSphere.setParent(self.lowerArmGroup)
		self.lowerCyl.setParent(self.lowerArmGroup)
		self.lowerArmGroup.setParent(self.baseGroup)
		
		self.upperArmGroup = viz.addGroup()
		self.upperSphere = vizshape.addSphere(radius = 5, slices = 20, stacks = 20)
		self.upperCyl = vizshape.addCylinder(height = 40, radius = 2.5, axis = vizshape.AXIS_Y, slices = 20, bottom = True, top = True)
		m = viz.Matrix()
		m.postTrans(0, 20, 0)
		self.upperCyl.setMatrix(m)
		
		self.upperSphere.setParent(self.upperArmGroup)
		self.upperCyl.setParent(self.upperArmGroup)
		self.upperArmGroup.setParent(self.lowerArmGroup)

		self.shadeGroup = viz.addGroup()
		self.shadeSphere = vizshape.addSphere(radius = 5, slices = 20, stacks = 20)
		self.shade = vizshape.addCone(radius = 20, height = 30)
		m = viz.Matrix()
		m.postTrans(0, -15, 0)
		m.postAxisAngle(0, 0, 1, 180)
		self.shade.setMatrix(m)
		
		self.shadeSphere.setParent(self.shadeGroup)
		self.shade.setParent(self.shadeGroup)
		self.shadeGroup.setParent(self.upperArmGroup)
		
		
		
		
		# set transformation group matrices of nodes to give 
		# desired configuration
		self.transform()
		
		# setup callback methods
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
		self.callback(viz.TIMER_EVENT,self.onTimer)

	# Sets the transformation matrices of the Luxo group 
	# nodes to achieve desired configuration
	def transform(self):
		m = viz.Matrix()
		m.postTrans(self.x, self.y)
		self.baseGroup.setMatrix(m)
		
		#lower arm
		m = viz.Matrix()
		m.postAxisAngle(0,0,1, self.a)
		m.postAxisAngle(0,1,0, self.b)
		m.postTrans(0, 5, 0)
		self.lowerArmGroup.setMatrix(m)
		
		#upper arm
		m = viz.Matrix()
		m.postAxisAngle(0,0,1, self.c)
		m.postTrans(0, 40, 0)
		self.upperArmGroup.setMatrix(m)
		
		m = viz.Matrix()
		m.postAxisAngle(0,0,1, self.d)
		m.postAxisAngle(0,1,0, self.e)
		m.postTrans(0, 40, 0)
		self.shadeGroup.setMatrix(m)
		
	# This gets executed whenever a key is pressed down.
	def onKeyDown(self,key):
		if key == ' ':
			self.starttimer(1, .10, 10)
		if (key == viz.KEY_RIGHT):
			self.x = self.x + 5
		if (key == viz.KEY_LEFT):
			self.x = self.x - 5	
		if (key == viz.KEY_DOWN):
			self.y = self.y - 5
		if (key == viz.KEY_UP):
			self.y = self.y + 5
		if (key == '1'):
			self.a = self.a + 5
		if (key == '2'):
			self.a = self.a - 5
		if (key == '3'):
			self.b = self.b + 5
		if (key == '4'):
			self.b = self.b - 5
		if (key == '5'):
			self.c = self.c + 5
		if (key == '6'):
			self.c = self.c - 5
		if (key == '7'):
			self.d = self.d + 5
		if (key == '8'):
			self.d = self.d - 5
		if (key == '9'):
			self.e = self.e + 5
		if (key == '0'):
			self.e = self.e - 5
		self.transform()
		
		if ( key == 'g' ):
			self.starttimer(1, 1/20.0, viz.FOREVER)

	# This gets executed whenever a timer event occurs.
	def onTimer(self,num):
		if num == 1:
			self.a += 5
		elif num == 2:
			self.a -= 5
		elif num == 3:
			self.b += 5
		elif num == 4:
			self.b -= 5
		elif num == 5:
			self.c += 5
		elif num == 6:
			self.c -= 5
		elif num == 7:
			self.d += 5
		elif num == 8:
			self.d -= 5
		elif num == 9:
			self.e += 5
		elif num == 10:
			self.e -= 5
			
		if self.animationCounter == 10:
			self.killtimer(num)
			self.starttimer(num + 1, .10, 10)
			self.animationCounter = 0
		else:
			self.animationCounter += 1
			
		self.transform()
		
# Luxo Driver Code
# set size (in pixels) and title of application window
viz.window.setSize( 500, 500 )
viz.window.setName( "Luxo" )

# get graphics window
window = viz.MainWindow
# setup viewing volume
window.ortho(-200,200,-200,200,-200,200)
# set background color of window to very light gray 
viz.MainWindow.clearcolor( [150,150,150] ) 
# center viewpoint 
viz.eyeheight(0)

c = Luxo()

# render the scene in the window
viz.go()
