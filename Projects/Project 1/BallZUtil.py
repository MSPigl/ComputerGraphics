# File: BallZUtil.py

import viz
import math
import random

# Launcher class inherits event handling methods from viz.EventClass
class Launcher:
	def __init__(self, angle, length):
		# Instance variables
		self.angle = angle
		self.changeInAngle = 0
		self.length = length
		
		self.x = 0
		self.y = -100
		
		viz.startLayer(viz.LINES)
		
		viz.vertexColor(1, 0, 0)
		viz.lineWidth(5)
		
		# Define vertices
		viz.vertex(0, 0)
		viz.vertex(math.cos(math.radians(self.angle)) * self.length, math.sin(math.radians(self.angle)) * self.length)
		
		# Capture layer and set its transformation matrix
		self.vertices = viz.endLayer()
		m = viz.Matrix()
		m.postTrans(self.x, self.y)
		self.vertices.setMatrix(m)
		
	def getX(self):
		return self.x + math.cos(math.radians(self.angle)) * self.length
		
	def getY(self):
		return self.y + math.sin(math.radians(self.angle)) * self.length
		
	def getAngle(self):
		return self.angle
		
	def rotateLeft(self):
		self.angle += 5
		self.changeInAngle += 5
		m = viz.Matrix()
		m.postAxisAngle(0, 0, 1, self.changeInAngle)
		m.postTrans(self.x, self.y)
		self.vertices.setMatrix(m)
		
	def rotateRight(self):
		self.angle -= 5
		self.changeInAngle -= 5
		m = viz.Matrix()
		m.postAxisAngle(0, 0, 1, self.changeInAngle)
		m.postTrans(self.x, self.y)
		self.vertices.setMatrix(m)
		
# Ball class inherits event handling methods from viz.EventClass
class Ball:

	# Constructor 
	def __init__(self, angle):
		
		# Initialize Ball Instance Variables
		# radius 
		self.radius = 3
		# number of sides of regular polygon representing the ball
		self.sides = 50
		# velocity vector describing its direction and speed
		self.angle = angle

		self.vy = math.sin(math.radians(angle)) * 2
		self.vx = math.cos(math.radians(angle)) * 2

		# center location 
		self.x = 0
		self.y = 0
		
		# create layer for a circle, centered at (0,0)
		viz.startLayer(viz.POLYGON)
		viz.vertexColor(1,1,0)
		for i in range(0, 360, 360/self.sides):
			x = math.cos( math.radians(i) ) * self.radius
			y = math.sin( math.radians(i) ) * self.radius
			viz.vertex(x, y)
		# saves layer of vertices in instance variable called vertices
		self.vertices = viz.endLayer()
		
	def getX(self):
		return self.x
		
	def getY(self):
		return self.y
		
	def getVX(self):
		return self.vx
		
	def getVY(self):
		return self.vy
		
	def setXY(self,x,y):
		self.x = x
		self.y = y
		
		m = viz.Matrix()
		m.postTrans(self.x, self.y)
		self.vertices.setMatrix(m)
		
		
	def setVXVY(self,vx,vy):
		self.vx = vx
		self.vy = vy
		
class Block:
	def __init__(self, row, col):
		# Length of each block
		self.length = 20
		
		# Instance variables
		self.x = (row * self.length) - 100
		self.y = 100 - (col * self.length)
		self.row = col
		self.col = row
		
		viz.startLayer(viz.POLYGON)
		
		# Assign vertices a random color
		viz.vertexColor(random.uniform(.2, 1),random.uniform(.2, 1), random.uniform(.2, 1))
		
		# Define vertices
		viz.vertex(0, 0)
		viz.vertex(self.length, 0)
		viz.vertex(self.length, -self.length)
		viz.vertex(0, -self.length)
		
		# Capture layer and set its transformation matrix
		self.vertices = viz.endLayer()
		m = viz.Matrix()
		m.postTrans(self.x, self.y)
		self.vertices.setMatrix(m)
		
	def getX(self):
		return self.x
		
	def getRow(self):
		return self.row
		
	def getCol(self):
		return self.col
		
	def shiftDown(self):
		self.y -= self.length
		self.row += 1
		m = viz.Matrix()
		m.postTrans(self.x, self.y)
		self.vertices.setMatrix(m)
		
	def contains(self, x, y):
		if x >= self.x and x <= self.x + self.length:
			if y >= self.y - self.length and y <= self.y:
				return True
		return False