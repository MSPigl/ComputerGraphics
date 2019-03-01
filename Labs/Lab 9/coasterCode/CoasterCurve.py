# This class represents the path of a roller coaster track. The path
# is composed of circular and straight pieces.
# Using its time features, it can be used to simulate the movement of
# a car traveling along the curve. It can provide both location and
# orientation information about the car. 
#
# Author: Robin Flatland
#

import math
from CurvePiece import *

class CoasterCurve():
	
	# Constructor 
	def __init__(self):
		self.curTime = 0   # in seconds
		self.curDist = 0   # in feet
		self.curSpeed = 5  # in feet/second
		self.curPiece = 0  # index of current piece of curve 
		
		# Build the curve out of six pieces
		horz = Piece1(0)
		firstQuarCir = Piece2( horz.getEndWorldDist() )
		secondQuarCir = Piece3( firstQuarCir.distEndWorld )
		firstHalfCircle = Piece4( secondQuarCir.distEndWorld )
		fullCircle = Piece5( firstHalfCircle.distEndWorld )
		horz2 = Piece6( fullCircle.distEndWorld )
		self.pieceList = [horz, firstQuarCir, secondQuarCir, firstHalfCircle, fullCircle, horz2]
				
		# get total length of the curve
		self.lengthTrack = self.pieceList[ len(self.pieceList) - 1 ].distEndWorld
			
	# Returns the point [x,y,z] on the curve at distance
	# dist from the start of the curve.
	#
	def getLocationAtDist(self, dist):
		for i in range( len(self.pieceList) ):
			p = self.pieceList[i]
			if ( p.getStartWorldDist() <= dist ) and ( dist < p.getEndWorldDist() ):
				return p.getLocation( dist )
		print( "Error in getLocationAtDist: dist outside of range dist = ", dist )
		return [0,0,0]
		
	# Returns a 4x4 matrix which can be used to rotate the car into proper
	# orientation for the point on the curve at distance dist from the start. 
	# To work correctly, the car in its model coordinate system must be centered 
	# at the origin and facing forward down the -Z axis. 
	#
	def getOrientAtDist(self, dist):
		for i in range( len(self.pieceList) ):
			p = self.pieceList[i]
			if ( p.getStartWorldDist() <= dist ) and ( dist < p.getEndWorldDist() ):
				return p.getOrient( dist )
		print( "Error in getOrientAtDist: dist outside of range dist = ", dist )
		return viz.Matrix()
	
	# Advances the simulation time by amt (in seconds). The amt may be negative,
	# in which case time goes backwards.
	#
	def advanceTime(self, amt):
		self.curSpeed = self.curSpeed + self.pieceList[self.curPiece].getAcceleration()*amt
		if self.curSpeed < 0:
			self.curSpeed = 0
		self.curDist = self.curDist + self.curSpeed*amt
		self.curTime = self.curTime + amt
				
		if (self.curDist >= self.lengthTrack) or (self.curDist < 0):
			self.resetTime()
		
		# determine current piece of the curve
		for i in range( len(self.pieceList) ):
			p = self.pieceList[i]
			if ( p.getStartWorldDist() <= self.curDist ) and ( self.curDist < p.getEndWorldDist() ):
				self.curPiece = i
				break
				
	# Resets the simulation time to 0, which restarts the simulation.
	#
	def resetTime(self):
		self.curTime = 0
		self.curDist = 0
		self.curSpeed = 5 #starting speed
		self.curPiece = 0
		
	# Based on the current simulation time, this method returns 
	# the current location [x,y,z] of the car on the curve.
	#
	def getCurLocation(self):
		return self.getLocationAtDist( self.curDist )
		
	# Based on the current simulation time, this method
	# returns a 4x4 matrix which can be used to rotate the car into proper
	# orientation for the current location of the car.  
	# To work correctly, the car in its model coordinate system must be centered 
	# at the origin and facing forward down the -Z axis. 
	#
	def getCurOrient(self):
		return self.getOrientAtDist( self.curDist )
		
	# Based on the current simulation time, this method returns
	# the distance of the car from the start of the curve.
	#
	def getCurDist(self):
		return self.curDist
		
	# Returns the current simulation time.
	#
	def getCurTime(self):
		return selt.curTime
		
	# Returns the current simulation speed.
	#
	def getCurSpeed(self):
		return self.curSpeed
		
	