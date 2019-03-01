# File: Controller.py

import viz
import vizinput
from BallZUtil import *

# Controller class inherits event handling methods from viz.EventClass
class Controller(viz.EventClass):
	
	def __init__(self):
		
		viz.EventClass.__init__(self)
		
		# Lists to hold blocks and balls
		self.ballList = []
		self.blockList = []
		self.blockSounds = ['block_break1.wav', 'block_break2.wav', 'block_break3.wav', 'block_break4.wav']
		
		# 2D Array to track occupied block positions 
		self.blockPositions = []
		for i in range(0, 10):
			arr = [0,0,0,0,0,0,0,0,0,0]
			self.blockPositions.append(arr)
		
		# Instance booleans
		self.mute = False
		self.charging = False
		self.failState = False
		self.shootable = True
		
		# Counters
		self.clickCount = 1
		self.worldMultiplier = 1
		self.ballsOnScreen = 0
		self.roundCount = 0
		self.chargeCount = 0
		self.contactCount = 0
		
		# Event listeners
		self.callback(viz.TIMER_EVENT, self.onTimer)
		self.callback(viz.KEYDOWN_EVENT, self.onKeyDown)
		self.callback(viz.KEYUP_EVENT, self.onKeyUp)
		
		# Game loop
		self.starttimer(1, 1/25, viz.FOREVER)
		
		# Define the launcher
		self.launcher = Launcher(90, 25)
		
		# Set up initial row of blocks
		self.addBlocks()
	
	# Function to handle the release of a key
	def onKeyUp(self, key):
		# If the spacebar was pressed and there are no balls on the screen
		if key == ' ' and self.ballsOnScreen == 0:
			# Stop the charging timer
			self.killtimer(3)
			self.chargeCount = 0
			self.charging = False
			
			# Create a Ball, set its center point to the endpoint of the launcher, and set its velocity
			ball = Ball(self.launcher.getAngle())
			ball.setXY(self.launcher.getX(), self.launcher.getY())
			ball.setVXVY(ball.getVX() * self.worldMultiplier, ball.getVY() * self.worldMultiplier)
			viz.playSound(self.pickSound(6))
			
			# Append ball to list
			self.ballList.append(ball)
			self.ballsOnScreen += 1
			
			# Create delay if launching more than a single ball
			if self.clickCount > 1:
				self.starttimer(2, .25, self.clickCount - 2)
	
	# Function to handle the key down event
	def onKeyDown(self,key):
		# If key is the spacebar
		if key == ' ' and self.shootable:
			self.shootable = False
			
			# Start charging the launcher
			self.charging = True
			self.worldMultiplier = 1
			self.starttimer(3, .50, 10)
		# Increase or decrease the velocity of the balls on screen (for debugging)
		elif key == viz.KEY_UP:
			for i in range(0, len(self.ballList)):
				self.ballList[i].vx *= 1.05
				self.ballList[i].vy *= 1.05
		elif key == viz.KEY_DOWN:
			for i in range(0, len(self.ballList)):
				self.ballList[i].vx *= .95
				self.ballList[i].vy *= .95
		# Rotate the launcher to the left 
		elif key == viz.KEY_LEFT and self.shootable:
			if self.launcher.getAngle() < 175:
				self.launcher.rotateLeft()
		# Rotate the launcher to the right
		elif key == viz.KEY_RIGHT and self.shootable:
			if self.launcher.getAngle() > 5:
				self.launcher.rotateRight()
		# Mute sound
		elif key == 's' or key == 'S':
			if self.mute:
				self.mute = False
			else:
				self.mute = True
	
	# Function to handle timers
	def onTimer(self, num):
		# Main game loop
		if num == 1:
			# Check for balls colliding with the window borders
			for i in range(0, len(self.ballList)):
				if self.ballList[i].x + self.ballList[i].radius >= 100:
					self.ballList[i].vx = abs(self.ballList[i].vx) * -1
					if not self.mute:
						viz.playSound(self.pickSound(1))
				elif self.ballList[i].x - self.ballList[i].radius <= -100:
					self.ballList[i].vx = abs(self.ballList[i].vx)
					if not self.mute:
						viz.playSound(self.pickSound(1))
				elif self.ballList[i].y + self.ballList[i].radius >= 100:
					self.ballList[i].vy = abs(self.ballList[i].vy) * -1
					if not self.mute:
						viz.playSound(self.pickSound(1))
				elif self.ballList[i].y <= -100 - self.ballList[i].radius:
					self.ballList.pop(i)
					self.ballsOnScreen -= 1
					# Shift all the blocks on screen down
					if self.ballsOnScreen == 0:
						for i in range (0, len(self.blockList)):
							localRow = self.blockList[i].getRow()
							localCol = self.blockList[i].getCol()
							self.blockPositions[localRow][localCol] = 0
							self.blockList[i].shiftDown()
							self.blockPositions[localRow + 1][localCol] = 1
							
							# Check if a block has reached the bottom of the window
							for z in range(0, len(self.blockList)):
								if self.blockList[z].getRow() == 9:
									self.failState = True
									# Prompt for restart or quit
									break
									print("You lost!")
									
						# Give the player another ball if they broke twice the amount of blocks as their number of balls
						if self.contactCount >= self.clickCount * 2:
							self.clickCount += 1
						self.contactCount = 0
						if not self.failState:
							self.addBlocks()
							self.roundCount += 1
					break
				# Check for balls colliding with blocks
				else:
					contact = False
					for j in range(0, len(self.blockList)):
						if self.blockList[j].contains(self.ballList[i].getX() + self.ballList[i].radius, self.ballList[i].getY()):
							self.ballList[i].vx = abs(self.ballList[i].vx) * -1
							contact = True
						elif self.blockList[j].contains(self.ballList[i].getX() - self.ballList[i].radius, self.ballList[i].getY()):
							self.ballList[i].vx = abs(self.ballList[i].vx)
							contact = True
						elif self.blockList[j].contains(self.ballList[i].getX(), self.ballList[i].getY() + self.ballList[i].radius):
							self.ballList[i].vy = abs(self.ballList[i].vy) * -1
							contact = True
						elif self.blockList[j].contains(self.ballList[i].getX(), self.ballList[i].getY() - self.ballList[i].radius):
							self.ballList[i].vy = abs(self.ballList[i].vy)
							contact = True
						
						# Remove block from position and block lists if hit
						if contact:
							self.contactCount += 1
							self.blockPositions[self.blockList[j].getRow()][self.blockList[j].getCol()] = 0
							self.blockList[j].vertices.remove()
							self.blockList.pop(j)
							viz.playSound(self.pickSound(2))
							break
		
				self.ballList[i].x += self.ballList[i].vx
				self.ballList[i].y += self.ballList[i].vy
		
				self.ballList[i].setXY(self.ballList[i].x, self.ballList[i].y)
		# Handle the pause between launching balls
		elif num == 2:
				ball = Ball(self.launcher.getAngle())
				ball.setXY(self.launcher.getX(), self.launcher.getY())
				self.ballList.append(ball)
				ball.setVXVY(ball.getVX() * self.worldMultiplier, ball.getVY() * self.worldMultiplier)
				self.ballsOnScreen += 1
				viz.playSound(self.pickSound(6))
		# Charge launcher
		elif num == 3:
			if self.charging:
				self.worldMultiplier += .25
				self.chargeCount += 1
				if self.chargeCount == 9:
					viz.playSound(self.pickSound(5))
					self.chargeCount = 0
				else:
					viz.playSound(self.pickSound(4))
		# Prompt player if they failed
		if self.failState:
			self.killtimer(1)
			response = vizinput.ask("You survived {} rounds. Play again?".format(self.roundCount))
			if response == 1:
				self.reset()
			else:
				viz.quit()
	
	# Function to add a row of blocks at the top of the screen
	def addBlocks(self):
		if self.blockPositions[9].count(1) > 0:
			self.shootable = False
			return
		numBlocks = random.randint(1, 8)
		for i in range(0, numBlocks):
			row = random.randint(0, 9)
			col = 1
			while(self.blockPositions[col][row] != 0):
				row = random.randint(0, 9)
			
			block = Block(row, col)
			self.blockList.append(block)
			self.blockPositions[col][row] += 1
		self.shootable = True
		viz.playSound(self.pickSound(3))
	
	# Function to handle sounds
	def pickSound(self, type):
		# Bounce off wall
		if type == 1:
			return 'bounce.wav'
		# Block break
		elif type == 2:
			index = random.randint(0, len(self.blockSounds) - 1)
			
			return self.blockSounds[index]
		# New row
		elif type == 3:
			return 'new_row.wav'
		# Launcher charging
		elif type == 4:
			return 'charging.wav'
		# Launcher fully charged
		elif type == 5:
			return 'charged.wav'
		# Launch a ball
		elif type == 6:
			return 'launch.wav'
		return ''
		
	# Resets the game
	def reset(self):
		self.mute = False
		self.failState = False
		self.shootable = True
		
		self.clickCount = 1
		self.ballsOnScreen = 0
		self.roundCount = 0
		
		for i in range(0, 10):
			for j in range(0, 10):
				self.blockPositions[i][j] = 0
				
		for i in range(0, len(self.blockList)):
			self.blockList[i].vertices.remove()
		self.blockList = []
		
		self.launcher.vertices.remove()
		self.launcher = Launcher(90, 25)
		
		self.starttimer(1, 1/25, viz.FOREVER)
		
		self.addBlocks()