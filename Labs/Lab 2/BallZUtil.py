import viz
import math

class Block:
	def __init__(self, length, colors, x, y):
		self.length = length
		self.colors = colors
		self.x = x
		self.y = y
		
		viz.startLayer(viz.POLYGON)
		
		viz.vertexColor(colors[0], colors[1], colors[2])
		viz.pointSize(1)
		
		viz.vertex(0, 0)
		viz.vertex(length, 0)
		viz.vertex(length, length)
				
		viz.vertex(0, length)
		
		
		viz.endLayer()
		
class Launcher:
	def __init__(self, angle, length):
		self.angle = angle
		self.length = length
		
		self.angle *= math.pi/180 	
		
		self.x = math.cos(angle) * length
		self.y = math.sin(angle) * length
		
		print("({}, {})".format(self.x, self.y))
		
		viz.startLayer(viz.LINES)
		
		viz.vertexColor(1, 0, 0)
		viz.lineWidth(10)
		
		viz.vertex(0,0)
		viz.vertex(self.x,self.y)
		
		
		viz.endLayer()
		
class Ball:
	def __init__(self,radius, x, y):
		self.radius = radius
		self.x = x
		self.y = y
		
		viz.startLayer(viz.POLYGON)
		viz.vertexColor(1,1,1)
		
		for i in range (0,360):
			temp = i * math.pi/180
			viz.vertex(math.cos(temp) * self.radius, math.sin(temp) * self.radius)
		
		viz.endLayer()
		