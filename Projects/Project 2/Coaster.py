# Matt Pigliavento
# Siena College, Fall 2017
# Coaster.py


import viz
import vizshape
import math

class Coaster(viz.EventClass):
	#Constructor
	def __init__(self):
		#Call the super-class' constructor
		viz.EventClass.__init__(self)
		
		# Group node to hold the track
		self.track = viz.addGroup()
		
		# Group nodes to hold the horizontal rail segments
		self.ceiling = viz.addGroup()
		self.floor = viz.addGroup()
		
		self.yPos = 0
		self.xPos = 0
		for i in range (0, 10):
			railTop = self.makeRail()
			railBottom = self.makeRail()
			m = viz.Matrix()
			m.postTrans(0, self.yPos, 0)
			railTop.setMatrix(m)
			railBottom.setMatrix(m)
			
			railTop.setParent(self.ceiling)
			railBottom.setParent(self.floor)
			
			self.yPos += 10
		
		# Add the cart model to the scene and set it to its initial position 	
		self.cart = viz.add('model.dae')
		m = viz.Matrix()
		m.postTrans(-9.6, 1, -2.5)
		m.postAxisAngle(0, 1, 0, 270)
		m.setScale(12,12,12)
		m.postTrans(-135,90,-107)
		self.cart.setMatrix(m)
		
		# Log the cart's coordinates in the scene
		self.cartX = self.cart.getPosition()[0]
		self.cartY = self.cart.getPosition()[1]
		self.cartZ = self.cart.getPosition()[2]
		self.cart.setParent(self.track)
		
		# Move the ceiling rail to its initial position
		m = viz.Matrix()
		m.postAxisAngle(0, 1, 0, 90)
		m.postAxisAngle(0, 0, 1, 90)
		m.postTrans(-80,73,0)
		self.ceiling.setMatrix(m)
		
		# Move the floor rail to its initial position
		m = viz.Matrix()
		m.postAxisAngle(0, 1, 0, 90)
		m.postAxisAngle(0, 0, 1, 90)
		m.postTrans(161,-73,0)
		self.floor.setMatrix(m)
		
		# Lists to hold the points of the curved rail segments
		self.topArcPath = []
		self.bottomArcPath = []
		
		# List to hold the angles of the 'curved' rails
		self.arcAngles = []
		
		# Number of points in the curve
		self.arcPoints = 0
		
		# Group nodes to hold the entire arc segment and the uppermost arc
		self.arcs = viz.addGroup()
		self.topArc = viz.addGroup()
		
		# Draws the upper arc
		self.yPos = 0
		self.xPos = 0
		
		# The curve becomes smoother with smaller step values
		self.step = 15
		self.circleRadius = 75
		self.theta = 0
		while self.theta <= 90:
			# Find the next coordinate on the circle
			x = self.circleRadius * math.cos(math.radians(self.theta))
			y = self.circleRadius * math.sin(math.radians(self.theta))
			
			# Find the slope of the line between the previous and next points
			slope = (y - self.yPos) / (x - self.xPos)
			
			# Find the angle of the line using the slope
			lineAngle = math.degrees(math.atan(slope))
			
			# Condition avoids drawing a single rail at the center of the circle
			if slope != 0:
				rail = self.makeRail()
				
				# Variables to hold the new coordinate after the rotations
				deltaX = self.xPos
				deltaY = self.yPos
				
				# Transform the rail into its proper position, and log the changes into deltaX and deltaY
				m = viz.Matrix()
				m.postAxisAngle(0, 1, 0, 90)
				deltaX = x * math.cos(math.radians(90))	
				
				m.postAxisAngle(0, 0, 1, 90)
				tempX = deltaX
				deltaX = deltaX * math.cos(math.radians(90)) - y * math.sin(math.radians(90))
				deltaY = tempX * math.sin(math.radians(90)) + y * math.cos(math.radians(90))
				
				m.postAxisAngle(0, 0, 1, lineAngle)
				tempX = deltaX
				deltaX = deltaX * math.cos(math.radians(lineAngle)) - deltaY * math.sin(math.radians(lineAngle))
				deltaY = tempX * math.sin(math.radians(lineAngle)) + deltaY * math.cos(math.radians(lineAngle))
				
				m.postTrans(self.xPos, self.yPos, 0)
				deltaX += self.xPos - 40
				deltaY += self.yPos
				
				rail.setMatrix(m)
				rail.setParent(self.topArc)

				self.topArcPath.append(deltaX)
				self.topArcPath.append(deltaY)
				self.arcAngles.append(lineAngle)
				self.arcPoints += 1
			
			self.xPos = x
			self.yPos = y
			self.theta += self.step
		
		# This is similar to the top arc, but with different coordinates and transformations	
		self.bottomArc = viz.addGroup()
		self.yPos = 0
		self.xPos = 0
		self.step = 15
		self.circleRadius = 75
		self.theta = 180
		while self.theta <= 270:
			x = self.circleRadius * math.cos(math.radians(self.theta))
			y = self.circleRadius * math.sin(math.radians(self.theta))
			slope = (y - self.yPos) / (x - self.xPos)
			lineAngle = math.degrees(math.atan(slope))
			#print("x = {} | y = {} | slope = {} | lineAngle = {}".format(x, y, slope, lineAngle))
			
			if slope != 0 and self.theta != 180:
				rail = self.makeRail()
				
				deltaX = self.xPos
				deltaY = self.yPos
				
				m = viz.Matrix()
				m.postAxisAngle(0, 1, 0, 90)
				deltaX = x * math.cos(math.radians(90))	
				
				m.postAxisAngle(0, 0, 1, 90)
				tempX = deltaX
				deltaX = deltaX * math.cos(math.radians(90)) - y * math.sin(math.radians(90))
				deltaY = tempX * math.sin(math.radians(90)) + y * math.cos(math.radians(90))
				
				m.postAxisAngle(0, 0, 1, lineAngle)
				tempX = deltaX
				deltaX = deltaX * math.cos(math.radians(lineAngle)) - deltaY * math.sin(math.radians(lineAngle))
				deltaY = tempX * math.sin(math.radians(lineAngle)) + deltaY * math.cos(math.radians(lineAngle))
				
				m.postTrans(self.xPos, self.yPos, 0)
				deltaX += self.xPos
				deltaY += self.yPos
				
				rail.setMatrix(m)
				rail.setParent(self.bottomArc)
				
				deltaX += 115
				deltaY += 35
				
				self.bottomArcPath.append(deltaX)
				self.bottomArcPath.append(deltaY)
				self.arcAngles.append(lineAngle)
				self.arcPoints += 1
			
			self.xPos = x
			self.yPos = y
			self.theta += self.step
		
		# Move the bottom arc segment into position 
		m = viz.Matrix()
		m.postTrans(150)
		self.bottomArc.setMatrix(m)
		
		self.topArc.setParent(self.arcs)
		self.bottomArc.setParent(self.arcs)
		
		# Shift the entire curved segment into position
		m = viz.Matrix()
		m.postTrans(-80)
		self.arcs.setMatrix(m)
		
		self.ceiling.setParent(self.track)
		self.arcs.setParent(self.track)
		self.floor.setParent(self.track)
			
		# Event listeners	
		self.callback(viz.TIMER_EVENT, self.onTimer)
		self.callback(viz.KEYDOWN_EVENT, self.onKeyDown)
		
		# Indices to track which array element to access  
		self.arcPathIndex = (self.arcPoints / 2) - 1;
		self.angleIndex = (self.arcPoints / 2) - 1;
		
		# Counters to shift cart positions correctly 
		self.rotationTally = 0
		self.animationCounter = 0
		self.positionTracker = 0
		
	# Function to handle key events	
	def onKeyDown(self, key):
		# Spacebar
		if key == ' ':
			# Start the animation
			self.starttimer(1, .1, 15)
	
	# Function to handle timer events		
	def onTimer(self, num):
		# Move along the top segment
		if num == 1:
			self.cart.setPosition(self.cart.getPosition()[0] + 5, self.cart.getPosition()[1], self.cart.getPosition()[2])
			
			# Star the next part of the animation
			if self.animationCounter == 15:
				self.killtimer(1)
				self.starttimer(2, .1, self.arcPoints)
				self.animationCounter = 0
			else:
				self.animationCounter += 1
		# Move cart along the top arc segment		
		elif num == 2:
			# Set cart position and rotation
			tempZ = self.cart.getPosition()[2]
			self.rotationTally += self.arcAngles[self.angleIndex]
			self.cart.setEuler(0, self.arcAngles[self.angleIndex], 0, viz.REL_LOCAL)
			self.cart.setPosition((self.topArcPath[self.arcPathIndex - 1]) - self.positionTracker * 10, (self.topArcPath[self.arcPathIndex]), tempZ)
			
			# Start the next part of the animation
			if self.arcPathIndex <= 1:
				self.killtimer(2)
				self.arcPathIndex = 2
				self.angleIndex = 0
				self.positionTracker = 0
				self.starttimer(3, .1, self.arcPoints)
			else:
				self.arcPathIndex -= 2
			self.angleIndex -= 1
			self.positionTracker += 1 
		# Move cart along the bottom arc segment
		elif num == 3:
			self.cart.setEuler(0, 15, 0, viz.REL_LOCAL)
			self.cart.setPosition((self.bottomArcPath[self.arcPathIndex]) - self.positionTracker * 18, (self.bottomArcPath[self.arcPathIndex + 1]), self.cart.getPosition()[2])
			
			# Start the next part of the animation 
			if self.arcPathIndex >= self.arcPoints / 2 + 1:
				self.killtimer(3)
				self.cart.setEuler(0, 5, 0, viz.REL_LOCAL)
				self.starttimer(4, .1, 21)
			else:
				self.arcPathIndex += 2
			self.angleIndex += 1
			self.positionTracker += 1 
		# Move the cart along the bottom segment
		elif num == 4:
			self.cart.setPosition(self.cart.getPosition()[0] + 5, self.cart.getPosition()[1], self.cart.getPosition()[2])
		print(self.cart.getPosition())
		
	# Function to make a single rail piece	
	def makeRail(self):
		rail = viz.addGroup()
		
		# Cylinders to act as the wheel tracks
		leftCyl = vizshape.addCylinder(height = 20, radius = 5, axis = vizshape.AXIS_Y, slices = 20, bottom = True, top = True)
		m = viz.Matrix()
		m.postTrans(-10)
		leftCyl.setMatrix(m)
		
		rightCyl = vizshape.addCylinder(height = 20, radius = 5, axis = vizshape.AXIS_Y, slices = 20, bottom = True, top = True)
		m = viz.Matrix()
		m.postTrans(10)
		rightCyl.setMatrix(m)
		
		# Slats
		slat1 = vizshape.addBox(size = (40, 5, 5), right = True, left = True, top = True, bottom = True, front = True, back = True, splitFaces = False)
		m = viz.Matrix()
		m.postTrans(0, 5, 0)
		slat1.setMatrix(m)
		
		slat2 = vizshape.addBox(size = (40, 5, 5), right = True, left = True, top = True, bottom = True, front = True, back = True, splitFaces = False)
		m = viz.Matrix()
		m.postTrans(0, -5, 0)
		slat2.setMatrix(m)
		
		leftCyl.setParent(rail)
		rightCyl.setParent(rail)
		slat1.setParent(rail)
		slat2.setParent(rail)
		
		return rail