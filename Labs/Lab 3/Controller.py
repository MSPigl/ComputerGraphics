# File: Controller.py

import viz
from Ball import *

# Controller class inherits event handling methods from viz.EventClass
class Controller(viz.EventClass):
	
	def __init__(self):
		
		# must call constructor of EventClass first!!
		viz.EventClass.__init__(self)
		
		self.ballList = []
		self.mute = False
		
		#self.ballList[i] = Ball()
		
		self.callback(viz.TIMER_EVENT, self.onTimer)
		self.callback(viz.KEYDOWN_EVENT, self.onKeyDown)
		
		self.starttimer(1, 1/25, viz.FOREVER)
		
	def onKeyDown(self,key):
		if key == ' ':
			ball = Ball()
			self.ballList.append(ball)
		elif key == viz.KEY_UP:
			for i in range(0, len(self.ballList)):
				self.ballList[i].vx *= 1.05
				self.ballList[i].vy *= 1.05
		elif key == viz.KEY_DOWN:
			for i in range(0, len(self.ballList)):
				self.ballList[i].vx *= .95
				self.ballList[i].vy *= .95
		elif key == 's' or key == 'S':
			if self.mute:
				self.mute = False
			else:
				self.mute = True
	
	def onTimer(self, num):
		for i in range(0, len(self.ballList)):
			if self.ballList[i].x + self.ballList[i].radius >= 100:
				self.ballList[i].vx = abs(self.ballList[i].vx) * -1
				if not self.mute:
					viz.playSound('bounce.wav')
			elif self.ballList[i].x - self.ballList[i].radius <= -100:
				self.ballList[i].vx = abs(self.ballList[i].vx)
				if not self.mute:
					viz.playSound('bounce.wav')
			elif self.ballList[i].y + self.ballList[i].radius >= 100:
				self.ballList[i].vy = abs(self.ballList[i].vy) * -1
				if not self.mute:
					viz.playSound('bounce.wav')
			elif self.ballList[i].y - self.ballList[i].radius <= -100:
				self.ballList[i].vy = abs(self.ballList[i].vy)
				if not self.mute:
					viz.playSound('bounce.wav')
		
			self.ballList[i].x += self.ballList[i].vx
			self.ballList[i].y += self.ballList[i].vy
		
			self.ballList[i].setXY(self.ballList[i].x, self.ballList[i].y)
		
		#print("Timer went off")
		#print("Center coordinates at ({}, {})".format(self.ballList[i].x, self.ballList[i].y))
	
		
	