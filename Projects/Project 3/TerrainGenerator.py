# File: TerrainGenerator.py
# Author: Matt Pigliavento
# Siena College, Fall 2017

import viz
import random
from math import pow

class TerrainGenerator(viz.EventClass):
	# Constructor for class TerrainGenerator
	def __init__(self):
		# Super-class constructor 
		viz.EventClass.__init__(self)
		
		# Fields to track the camera position
		self.rotateView = 45
		self.heightView = 50
		self.distView = 0
		
		# Fields to track the position of the plane
		self.planeAngle = 0
		self.planeY = 0
		self.planeZ = 0
		self.spinAngle = 0
		
		self.view = 1
		
		# Get input from user to determine grid size
		self.k = int(input("Enter k -> "))
		self.size = int(pow(2, self.k) + 1)
		print("k is {} | size is {}".format(self.k, self.size))
		
		# Get heightmap
		self.grid = self.diamondSquare(self.size)#, 100, 100, 100, 100)
		
		# Print grid if less than or equal to 9x9
		if self.k <= 3:
			self.printGrid(self.grid)
			
		self.max = self.grid[0][0]
		self.min = self.grid[0][0]
		
		# Find the maximum and minimum values
		for row in range(0, self.size):
			for col in range(0, self.size):
				if self.grid[row][col] > self.max:
					self.max = self.grid[row][col]
				
				if self.grid[row][col] < self.min:
					self.min = self.grid[row][col]
		
		# Layer to hold the heightmap
		viz.startLayer(viz.TRIANGLES)
		for row in range(0, self.size - 1):
			for col in range(0, self.size - 1):
				val = self.grid[row][col]
				viz.vertexColor((val - self.min) / (self.max - self.min), (val - self.min) / (self.max - self.min), (val - self.min) / (self.max - self.min))
				viz.vertex(col * 10, val, row * 10)
				viz.vertex(col * 10, self.grid[row + 1][col], (row + 1) * 10)
				viz.vertex((col + 1) * 10, self.grid[row][col + 1], row * 10)
				
				viz.vertex(col * 10, self.grid[row + 1][col], (row + 1) * 10)
				viz.vertex((col + 1) * 10, self.grid[row + 1][col + 1], (row + 1) * 10)
				viz.vertex((col + 1) * 10, self.grid[row][col + 1], row * 10)
				
		self.terrain = viz.endLayer()
		
		# Add skybox to scene
		sky = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
		skybox = viz.add('skydome.dlc')
		skybox.texture(sky)
		
		# Add fighter jet to scene
		self.plane = viz.add('./F-15C_Eagle/F-15C_Eagle.3ds')
		
		# Initialize plane's position 
		self.planeY = self.grid[0][0] + 10
		self.plane.setPosition(0, self.planeY, 0)
		
		# Position the camera's Y-value to the value at origin 
		self.heightView = self.grid[0][0]
		
		# Set keyboard callback function
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
			
		self.callback(viz.TIMER_EVENT,self.onTimer)
		
		# Call keyboard callback to initialize the view to 3rd person
		self.onKeyDown("1")
		
	
	# Function to generate and return a heightmap stored as a two-dimensional list
	# gridSize: the size of the NxN grid
	# topLeftSeed: the value used to seed the top-left corner 
	# topRightSeed: the value used to seed the top-right corner 
	# botLeftSeed: the value used to seed the bottom-left corner
	# botRightSeed: the value used to seed the bottom-right corner
	def diamondSquare(self, gridSize = 3, topLeftSeed = 100, topRightSeed = 75, botLeftSeed = 50, botRightSeed = 25):
		grid = [[-1.0 for x in range(gridSize)] for y in range(gridSize)]
		
		# Seed the corners
		grid[0][0] = topLeftSeed
		grid[0][gridSize - 1] = topRightSeed
		grid[gridSize - 1][0] = botLeftSeed
		grid[gridSize - 1][gridSize - 1] = botRightSeed
		
		sideLength = gridSize - 1
		
		# Main loop
		while sideLength > 1:
			halfStep = sideLength / 2
			
			# Diamond step
			for i in range(0, gridSize - 1, sideLength):
				for j in range (0, gridSize - 1, sideLength):
					topLeft = grid[i][j]                            #top left
					topRight = grid[i + sideLength][j]              #top right
					botLeft = grid[i][j + sideLength]               #bottom left
					botRight = grid[i + sideLength][j + sideLength] #bottom right
					
					avg = (topLeft + topRight + botLeft + botRight) / 4.0
					
					grid[i + halfStep][j + halfStep] = avg
			
			# Square step
			for i in range(0, gridSize, halfStep):
				for j in range ((i + halfStep) % sideLength, gridSize, sideLength):
					validPoints = 0
					
					left = grid[i - halfStep][y] if i - halfStep >= 0 else 0
					right = grid[i + halfStep][y] if i + halfStep < gridSize else 0
					top = grid[i][j + halfStep] if j + halfStep < gridSize else 0
					bottom = grid[i][j - halfStep] if j - halfStep >= 0 else 0
					
					if left > 0:
						validPoints += 1
					if right > 0:
						validPoints += 1
					if top > 0:
						validPoints += 1
					if bottom > 0:
						validPoints += 1
						
					avg = (left + right + top + bottom) / validPoints
					
					grid[i][j] = avg
					
			sideLength /= 2
		
		return grid
		
	# Function to handle timer events
	def onTimer(self, num):
		if num == 1:
			self.spinAngle += 5
			
			theta = self.planeAngle - self.planeAngle if self.planeAngle > 0 else self.planeAngle + self.planeAngle
			
			m = viz.Matrix()
			m.postAxisAngle(0, 1, 0, theta)
			m.postTrans(0, self.planeY - self.planeY if self.planeY > 0 else self.planeY + self.planeY,
			self.planeZ - self.planeZ if self.planeZ > 0 else self.planeZ + self.planeZ)
			m.postAxisAngle(0, 0, 1, self.spinAngle)
			m.postTrans(0,self.planeY, self.planeZ) 
			self.plane.setMatrix(m)
		
	# Function to handle key-down events
	def onKeyDown(self,key):
		# Controls for first person view
		if (key == "1"):
			self.view = 1
		elif (key == viz.KEY_LEFT):
			self.rotateView -= 1
		elif (key == viz.KEY_RIGHT):
			self.rotateView += 1
		elif (key == viz.KEY_UP):
			self.distView += 1
		elif (key == viz.KEY_DOWN):
			self.distView -= 1
		elif (key == 'u'):
			self.heightView += 1
		elif (key =='d'):
			self.heightView -= 1
		
		# Controls for plane view
		if (key == "3"):
			self.view = 3
		elif (key == viz.KEY_LEFT):
			self.planeAngle -= 1
		elif (key == viz.KEY_RIGHT):
			self.planeAngle += 1
		elif (key == viz.KEY_UP):
			self.planeZ += 2
		elif (key == viz.KEY_DOWN):
			self.planeZ -= 2
		elif (key == 'u'):
			self.planeY += 2
		elif (key =='d'):
			self.planeY -= 2
		
		# Makes the plane perform a barrel role
		if (key == ' '):
			self.spinAngle = 0
			self.starttimer(1, viz.FASTEST_EXPIRATION, 71)
			
		# Transforms the camera
		if (self.view == 1):
			# set camera view for 3rd person 
			view = viz.MainView
			m = viz.Matrix()
			m.postTrans(0,self.heightView,self.distView)
			m.postAxisAngle( 0,1,0, self.rotateView)
			view.setMatrix(m)
		elif (self.view == 3):
			view = viz.MainView
			m = viz.Matrix()
			m.postTrans(0,self.planeY + 5, self.planeZ - 35) 
			m.postAxisAngle(0,1,0, self.planeAngle)
			view.setMatrix(m)
			
			m = viz.Matrix()
			m.postTrans(0,self.planeY, self.planeZ)
			m.postAxisAngle(0,1,0, self.planeAngle)
			m.postAxisAngle(0, 0, 1, self.spinAngle)
			self.plane.setMatrix(m)
			
	# Function to print a two-dimensional list
	def printGrid(self, grid):
		for row in grid:
			for e in row:
				print e,
			print
		print