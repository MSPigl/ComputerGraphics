from diamondSquare import *
import viz
import vizshape
import math

# Author: R. Flatland
# Controls the generation, display, and navigation of a terrain.

class TerrainController(viz.EventClass):
	
	def __init__(self):
		viz.EventClass.__init__(self)
			
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
				
		# generate random terrain using diamond-square algorithm
		self.terrainData = diamondSquare(7)
				
		# add some craters to the terrain
		self.makeCrater( self.terrainData, len(self.terrainData)/4, len(self.terrainData)/4, 10)
		self.makeCrater( self.terrainData, 6*len(self.terrainData)/8, len(self.terrainData)/2, 22)
				
		# create a triangular mesh (a Vizard layer of triangles) out of the data
		terrainLayer = self.generateLayer(self.terrainData)
		terrainLayer.enable(viz.LIGHTING)
		# viewer is located at (self.x,self.y,self.z)
		self.x = 0
		self.y = self.terrainData[0][0] + 1
		self.z = 0
		# viewer is rotated by self.rotate, an angle measured off the +x axis,
		# so initially the viewer is looking down the +z axis
		self.rotate = 90 
		# initialize this starting view 
		self.setView()
		
		viz.MainView.getHeadLight().disable()
		
		self.myLight = viz.addLight()
		self.myLight.enable()
		self.myLight.color(1,1,1)
		m = viz.Matrix()
		m.postAxisAngle(1,0,0,45)
		self.myLight.setMatrix(m)
		#print self.normal([1,1830,1],[2,1820,2], [2,1835,1])
		
		for row in self.terrainData:
			for col in row:
				print(col),
			print()
	
	# Input: a 2D square array containing elevation data 
	# Returns: a Vizard layer which is a triangular mesh 
	# representing the surface of the terrain 
	def generateLayer( self, terrainData ):
		viz.startLayer(viz.TRIANGLES)
		for r in range(0, len(terrainData)-1):
			for c in range(0, len(terrainData)-1):
				# each array location generates two triangles
				
				viz.vertexColor( viz.WHITE )
				# corners of first triangle, in ccw order when looking down on the surface
				c1 = [c, terrainData[r][c], r]
				c2 = [c+1, terrainData[r+1][c+1], r+1]
				c3 = [c, terrainData[r+1][c], r+1]
				
				viz.normal(self.normal(c1,c2,c3))

				viz.vertex(c1)
				viz.vertex(c2)
				viz.vertex(c3)
				
				viz.vertexColor( viz.WHITE )
				# corners of second triangle, in ccw order when looking down on the surface
				c1 = [c, terrainData[r][c], r]
				c2 = [c+1, terrainData[r][c+1], r]
				c3 = [c+1, terrainData[r+1][c+1], r+1]
				
				viz.normal(self.normal(c1,c2,c3))

				viz.vertex(c1)
				viz.vertex(c2)
				viz.vertex(c3)
				
		return viz.endLayer()
		

	# Keyboard call back method which controlls navigation over
	# the terrain using the arrow keys.
	def onKeyDown(self,key):
		if (key == viz.KEY_LEFT): # rotate viewer to the left
			self.rotate += 3
			self.setView()
		elif (key == viz.KEY_RIGHT): # rotate viewer to the right
			self.rotate -= 3
			self.setView()
		elif (key == viz.KEY_UP): # move viewer forward
			self.x += math.cos(math.radians(self.rotate))*.15
			self.z += math.sin(math.radians(self.rotate))*.15
			
			row = int(math.floor(self.x))
			col = int(math.floor(self.z))

			p = [row, self.terrainData[row][col], col]
			#v = [self.x, self.y, self.z]
			
			c1 = [col, self.terrainData[row][col], row]
			c2 = [col + 1, self.terrainData[row + 1][col + 1], row + 1]
			c3 = [col, self.terrainData[row + 1][col], row + 1]
			
			n = self.normal(c1, c2, c3)
			
			self.y = ((n[0]*p[0] - n[0]*self.x + n[1]*p[1] + n[2]*p[2] - n[2]*self.z) / n[1]) + 1
			print ("normal is {}".format(n))
			print((-5*2 - -5*1.8 + 1*1835 + 15*1 - 15*1.2)/1)
			print("Y is {}".format(self.y))
			print("Height at [{},{}] is {}".format(row, col, self.terrainData[row][col]))
			
			self.setView()
		elif (key == viz.KEY_DOWN): # move viewer backward
			self.x -= math.cos(math.radians(self.rotate))*.15
			self.z -= math.sin(math.radians(self.rotate))*.15
			
			row = int(math.floor(self.x))
			col = int(math.floor(self.z))

			p = [row, self.terrainData[row][col], col]
			#v = [self.x, self.y, self.z]
			
			c1 = [col, self.terrainData[row][col], row]
			c2 = [col + 1, self.terrainData[row + 1][col + 1], row + 1]
			c3 = [col, self.terrainData[row + 1][col], row + 1]
			
			n = self.normal(c1, c2, c3)
			
			self.y = ((n[0]*p[0] - n[0]*self.x + n[1]*p[1] + n[2]*p[2] - n[2]*self.z) / n[1]) + 1
			
			self.setView()
		elif (key == "u"): # move viewer up
			self.y += .5
			self.setView()
		elif (key == "d"): # move viewer down
			self.y -= .5
			self.setView()
		elif (key == "o"): # give viewer an overhead view
			view = viz.MainView
			mat = viz.Matrix()
			mat.postAxisAngle(1,0,0,90)
			mat.postTrans(+50,250,+50)
			view.setMatrix(mat)
	
	
	# Sets the current view using self.x, self.y, self.z as the
	# camera location and self.rotate as its rotation about the Y
	# axis.  The rotation is measured from the +x axis.
	def setView(self):
		view = viz.MainView
		mat = viz.Matrix()
		mat.postAxisAngle(0,1,0,90-self.rotate)
		mat.postTrans(self.x, self.y, self.z)
		view.setMatrix(mat)
		
	# Input: a 2D square array of elevation data, a center point
	# (cr,cc) and a radius for the crater.
	# Output: The 2D array is modified such that a crater at
	# the given location and radius is created.  
	def makeCrater(self, data, cr, cc, radius):
		for r in range(0, len(data)):
			for c in range(0, len(data)):
				dist = math.sqrt((r - cr)*(r - cr) + (c - cc)*(c - cc))
				if (dist < radius):
					y = math.sqrt( radius*radius - dist*dist )
					data[r][c] -= y/5.0
	
	
	def normal(self,c1,c2,c3):
		
		a = [c2[0] - c1[0], c2[1] - c1[1],c2[2] - c1[2]]
		b = [c3[0] - c1[0], c3[1] - c1[1],c3[2] - c1[2]]
		
		return [-(a[1]*b[2] - a[2]*b[1]), a[0]*b[2] - a[2]*b[0], -(a[0]*b[1] - a[1]*b[0])]
		
	