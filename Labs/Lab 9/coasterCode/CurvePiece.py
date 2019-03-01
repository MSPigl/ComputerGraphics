# These are the six pieces of the coaster curve

import math
import viz

class CurvePiece():
	
	# Constructor
	def __init__(self, distStartWorld, distEndWorld, acc, up):
		# distance from start of coaster to beginning of this piece
		self.distStartWorld = distStartWorld
		# distance from start of coaster to end of this piece
		self.distEndWorld = distEndWorld
		self.up = up
		self.acceleration = acc
		
	def getAcceleration(self):
		return self.acceleration
		
	def getStartWorldDist(self):
		return self.distStartWorld
		
	def getEndWorldDist(self):
		return self.distEndWorld
	
	def unitVector(self,a):
		vl = math.sqrt( a[0]*a[0] + a[1]*a[1] + a[2]*a[2] )
		return [a[0]/vl, a[1]/vl, a[2]/vl ]
		
	def crossProductUnit(self, a, b):
		c = [0,0,0]
		c[0] = a[1]*b[2] - a[2]*b[1]
		c[1] = -(a[0]*b[2] - a[2]*b[0])
		c[2] = a[0]*b[1] - a[1]*b[0]
		c = self.unitVector( c )
		return c
		
		
		
# horizontal stretch of track at beginning
# it is 100 feet long and runs from (-150,50) to (-50,0)
class Piece1( CurvePiece ):

	# Constructor
	def __init__( self, distStartWorld ):
		self.length = 100
		self.startPt = [-150,50,0]
		self.endPt = [-50,50,0]
		CurvePiece.__init__( self, distStartWorld, distStartWorld+self.length, 0, [0,1,0] )
	
	def getLength(self):
		return self.length
		
	def getLocation(self, dist ):
		if ( self.distStartWorld <= dist ) and ( dist < self.distEndWorld ):
			modelDist = dist - self.distStartWorld
			return [ self.startPt[0] + modelDist, self.startPt[1], self.startPt[2] ]
		else:
			print( "ERROR in getLocation Piece1: distance out of range" )
			exit()
			
		
	def getOrient(self, dist ):
		m = viz.Transform()
		m.set( 0,0,1,0, 0,1,0,0, -1,0,0,0, 0,0,0,1 ) 
		return m
		
# C1 quadrant of a circle centered at [-50, 0, 0] and in XY plane
# d=0 is top, d = 2PIr is right
class Piece2( CurvePiece ):

	# Constructor
	def __init__( self, distStartWorld ):
		self.radius = 50
		self.length = 2 * math.pi *self.radius / 4.0
		self.xtranslate = -50
		CurvePiece.__init__( self, distStartWorld, distStartWorld+self.length, .5, [.7071,.7071,0] )
	
	def getLength(self):
		return self.length
		
	def getLocation(self, distWorld ):
		if ( self.distStartWorld <= distWorld ) and ( distWorld < self.distEndWorld ):
			d = distWorld - self.getStartWorldDist()
			theta = (1 - d / self.length) * 90
			#print "d= ", d, "  theta = ", theta, " len = ", self.length
			x = self.radius * math.cos( math.radians( theta ) )
			y = self.radius * math.sin( math.radians( theta ) )
			return [ x + self.xtranslate, y, 0 ]	
		else:
			print( "ERROR in getLocation Piece2: distance out of range" )
			exit()
			
		
	def getOrient(self, distWorld ):
		if ( self.distStartWorld <= distWorld ) and ( distWorld < self.distEndWorld ):
			d = distWorld - self.getStartWorldDist()
			theta = (1 - d / self.length) * 90
			tF = [math.sin(math.radians(theta)), -math.cos(math.radians(theta)),0]
			tL = self.crossProductUnit( tF, self.up )
			tU = self.crossProductUnit( tL, tF )
			m = viz.Transform()
			m.set( tL[0],tL[1],tL[2],0,  tU[0],tU[1],tU[2],0,  -tF[0],-tF[1],-tF[2],0,  0,0,0,1 ) 
			return m
		else:
			print( "ERROR in getOrient Piece2: distance out of range" )
			exit()
		
	
# C3 quadrant of a circle centered at [50, 0, 0] and in XY plane
# d=0 is left side, d = 2PIr is on bottom
class Piece3( CurvePiece ):

	# Constructor
	def __init__( self, distStartWorld ):
		self.radius = 50
		self.length = 2 * math.pi *self.radius / 4.0
		self.xtranslate = 50
		#print( "piece 3 constuction start = ", distStartWorld, " end " , distStartWorld+self.length)
		CurvePiece.__init__( self, distStartWorld, distStartWorld+self.length, .8, [.7071,.7071,0] )
	
	def getLength(self):
		return self.length
		
	def getLocation(self, distWorld ):
		if ( self.distStartWorld <= distWorld ) and ( distWorld < self.distEndWorld ):
			d = distWorld - self.getStartWorldDist()
			theta = 180 + d / self.length * 90
			x = self.radius * math.cos( math.radians( theta ) )
			y = self.radius * math.sin( math.radians( theta ) )
			return [ x + self.xtranslate, y, 0 ]	
		else:
			print( "ERROR in getLocation Piece3: distance out of range" )
			exit()
			
		
	def getOrient(self, distWorld ):
		if ( self.distStartWorld <= distWorld ) and ( distWorld < self.distEndWorld ):
			d = distWorld - self.getStartWorldDist()
			theta = 180 + d / self.length * 90
			tF = [-math.sin(math.radians(theta)), math.cos(math.radians(theta)),0]
			tL = self.crossProductUnit( tF, self.up )
			tU = self.crossProductUnit( tL, tF )
			m = viz.Transform()
			m.set( tL[0],tL[1],tL[2],0,  tU[0],tU[1],tU[2],0,  -tF[0],-tF[1],-tF[2],0,  0,0,0,1 ) 
			return m
		else:
			print( "ERROR in getOrient Piece2: distance out of range" )
			exit()
			
			
# C2,C1 quadrant of a horizontal circle centered at [50, -50, -50] and in XY plane
# d=0 is left side, d = 2PIr/2 is right side
class Piece4( CurvePiece ):

	# Constructor
	def __init__( self, distStartWorld ):
		self.radius = 50
		self.length = 2 * math.pi *self.radius / 2.0
		self.xtranslate = 50
		self.ytranslate = -50
		self.ztranslate = -50
		self.roll = 70
		print( "piece 4 constuction start = ", distStartWorld, " end " , distStartWorld+self.length)
		CurvePiece.__init__( self, distStartWorld, distStartWorld+self.length, 0, [0,1,0] )
	
	def getLength(self):
		return self.length
		
	def getLocation(self, distWorld ):
		if ( self.distStartWorld <= distWorld ) and ( distWorld < self.distEndWorld ):
			d = distWorld - self.getStartWorldDist()
			theta = d / self.length * 180
			z = self.radius * math.cos( math.radians( theta ) )
			x = self.radius * math.sin( math.radians( theta ) )
			return [ x + self.xtranslate, self.ytranslate, z+self.ztranslate ]	
		else:
			print( "ERROR in getLocation Piece3: distance out of range" )
			exit()
			
		
	def getOrient(self, distWorld ):
		if ( self.distStartWorld <= distWorld ) and ( distWorld < self.distEndWorld ):
			d = distWorld - self.getStartWorldDist()
			theta = d / self.length * 180
			tF = [math.cos(math.radians(theta)), 0, -math.sin(math.radians(theta))]
			tL = self.crossProductUnit( tF, self.up )
			tU = self.crossProductUnit( tL, tF )
			m = viz.Transform()
			m.set( tL[0],tL[1],tL[2],0,  tU[0],tU[1],tU[2],0,  -tF[0],-tF[1],-tF[2],0,  0,0,0,1 )
			r = d / self.length * self.roll
			m.postAxisAngle( tF[0], tF[1], tF[2], -r )
			return m
		else:
			print( "ERROR in getOrient Piece2: distance out of range" )
			exit()
			
			
# Full horizontal circle centered at [50, -50, -50] and in XY plane
# with z value decreasing. d=0 is right side, d = 2PIr/2 is left side
class Piece5( CurvePiece ):

	# Constructor
	def __init__( self, distStartWorld ):
		self.radius = 50
		self.length = 2 * math.pi *self.radius 
		self.xtranslate = 50
		self.ytranslate = -50
		self.ztranslate = -50
		self.roll = 70
		self.zchange = -50
		#print( "piece 4 constuction start = ", distStartWorld, " end " , distStartWorld+self.length)
		CurvePiece.__init__( self, distStartWorld, distStartWorld+self.length, .2, [0,1,0] )
	
	def getLength(self):
		return self.length
		
	def getLocation(self, distWorld ):
		if ( self.distStartWorld <= distWorld ) and ( distWorld < self.distEndWorld ):
			d = distWorld - self.getStartWorldDist()
			theta = 180 + d / self.length * 360
			z = self.radius * math.cos( math.radians( theta ) )
			x = self.radius * math.sin( math.radians( theta ) )
			y = d/self.length*self.zchange
			print [ x + self.xtranslate, y + self.ytranslate, z+self.ztranslate ]	
			return [ x + self.xtranslate, y + self.ytranslate, z+self.ztranslate ]	
		else:
			print( "ERROR in getLocation Piece3: distance out of range" )
			exit()
			
		
	def getOrient(self, distWorld ):
		if ( self.distStartWorld <= distWorld ) and ( distWorld < self.distEndWorld ):
			d = distWorld - self.getStartWorldDist()
			theta = 180 + d / self.length * 360
			tF = [math.cos(math.radians(theta)), self.zchange/self.length, -math.sin(math.radians(theta))]
			tF = self.unitVector(tF)
			tL = self.crossProductUnit( tF, self.up )
			tU = self.crossProductUnit( tL, tF )
			m = viz.Transform()
			m.set( tL[0],tL[1],tL[2],0,  tU[0],tU[1],tU[2],0,  -tF[0],-tF[1],-tF[2],0,  0,0,0,1 )
			m.postAxisAngle( tF[0], tF[1], tF[2], -self.roll )
			return m
		else:
			print( "ERROR in getOrient Piece2: distance out of range" )
			exit()
		
# Horizontal stretch at end, length 100
class Piece6( CurvePiece ):

	# Constructor
	def __init__( self, distStartWorld ):
		self.length = 200
		self.startPt = [50,-100,-100]
		self.endPt = [-50,-100,-100]
		self.roll = 70
		CurvePiece.__init__( self, distStartWorld, distStartWorld+self.length, -2.2, [0,1,0] )
	
	def getLength(self):
		return self.length
		
	def getLocation(self, distWorld ):
		if ( self.distStartWorld <= distWorld ) and ( distWorld < self.distEndWorld ):
			modelDist = distWorld - self.distStartWorld
			return [ self.startPt[0] - modelDist, self.startPt[1], self.startPt[2] ]
		else:
			print( "ERROR in getLocation Piece1: distance out of range" )
			exit()
			
		
	def getOrient(self, dist ):
		d = dist - self.getStartWorldDist()
		m = viz.Transform()
		m.postAxisAngle(0,1,0,90)
		r = self.roll - self.roll * 3*d / self.length
		if r < 0:
			r = 0
		#print "r = ", r
		m.postAxisAngle(1,0,0,r)
		#m.set( 0,0,1,0, 0,1,0,0, -1,0,0,0, 0,0,0,1 ) 
		#m.postAxisAngle( -1, 0, 0, -self.roll )
		return m
		
	