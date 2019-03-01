import viz
import vizshape
import math

class ZoneController(viz.EventClass):
	
	def __init__(self):
		viz.EventClass.__init__(self)
		
		self.zones = []
		for i in range(1, 101):
			self.zones.append(Zone(myId = i, center = [0, 0, i * 100], zoneRadius = 50.0, zoneHeight = 25))
		
		for obj in self.zones:
			obj.zone.color(r = 0, g = 1.0, b = 0)
			obj.zone.alpha(0.8)
			
			obj.zone.setPosition(obj.getCenter())
		
		self.player = vizshape.addBox(size = [5, 5, 5])
		self.player.color([1, 0, 0])
		
		self.playerX = 0
		self.playerY = 0
		self.playerZ = 0
		
		self.inId = 0
		
		self.callback(viz.KEYDOWN_EVENT, self.onKeyDown)
		self.onKeyDown(' ')
		
		self.callback(viz.TIMER_EVENT, self.onTimer)
		self.starttimer(1, viz.FASTEST_EXPIRATION, viz.FOREVER)
		
	def onKeyDown(self, key):
		if key == viz.KEY_UP:
			self.playerZ += 5
		elif key == viz.KEY_DOWN:
			self.playerZ -= 5
		
		if key == viz.KEY_LEFT:
			self.playerX -= 5
		elif key == viz.KEY_RIGHT:
			self.playerX += 5
			
		m = viz.Matrix()
		m.postTrans(self.playerX, self.playerY, self.playerZ)
		self.player.setMatrix(m)
		
		view = viz.MainView
		viewMat = viz.Matrix()
		viewMat.postAxisAngle(1, 0, 0, 90)
		viewMat.postTrans(self.playerX, self.playerY + 500, self.playerZ)
		
		view.setMatrix(viewMat)
		
	def onTimer(self, num):
		for obj in self.zones:
			if (self.inCircle(obj.getRadius(), self.playerX, self.playerY, self.playerZ, 
			obj.getCenter()[0], obj.getCenter()[1], obj.getCenter()[2])):
				obj.occupied = True
				break
			else:
				obj.occupied = False
		
		self.zones[self.inId].zone.color([0, 1, 0])
		self.inId = obj.getId() - 1
		self.zones[self.inId].zone.color([1, 0, 0])
	
	def inCircle(self, rad, point_x, point_y, point_z, center_x, center_y, center_z):
		dist = math.sqrt(math.pow(point_x - center_x, 2) + math.pow(point_y - center_y, 2) + math.pow(point_z - center_z, 2))
		
		if dist <= rad:
			return True
		return False
			
class Zone():
	def __init__(self, myId, center, zoneRadius, zoneHeight):
		self.zone = vizshape.addCylinder(height = zoneHeight, radius = zoneRadius, slices = 500)
		self.x, self.y, self.z = center[0], center[1], center[2]
		self.radius = zoneRadius
		self.id = myId
		self.occupied = False
		
	def getRadius(self):
		return self.radius
		
	def getId(self):
		return self.id
		
	def setCenter(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		
	def getCenter(self):
		return [self.x, self.y, self.z]