#Chris Fall and Matt Pigliavento
import viz
import vizshape
import math
import random

class Controller(viz.EventClass):
	
	def __init__(self):
		
		viz.EventClass.__init__(self)
				
		self.callback(viz.TIMER_EVENT, self.onTimer)
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
		self.callback(viz.MOUSEDOWN_EVENT, self.onClick)
		self.callback(viz.COLLIDE_BEGIN_EVENT, self.onCollide)
		
		self.x = 0
		self.y = 0
		self.z = 0
		
		self.scaleValue = 2
		
		self.roll = 0
		self.pitch = 0
		self.yaw = 0
		
		self.rotateValue = 3

		self.numLives = 5
		
		self.t = viz.addText("Lives: " + str(self.numLives), viz.SCREEN, pos = [0,0.9,0])
		self.t.font('Times New Roman')
		self.t.fontSize(20)
		
		self.winText = viz.addText3D("You survived the trench!\n   Press any key to quit", viz.SCREEN, pos = [0.1,0.9,0], scene = viz.Scene2)
		self.winText.font('Times New Roman')
		self.winText.color(viz.YELLOW)
		
		self.loseText = viz.addText3D("   You died horribly!\n Press any key to quit", viz.SCREEN, pos = [0.15,0.9,0], scene = viz.Scene3)
		self.loseText.font('Times New Roman')
		self.loseText.color(viz.YELLOW)
		
		self.sounds = ['audio/XWING/XWing-Fly1.wav', 'audio/XWING/XWing-Fly2.wav', 'audio/XWING/XWing-Fly3.wav', 
		'audio/XWING/YWing-Fly1.wav', 'audio/XWING/YWing-Fly2.wav', 'audio/TIE/TIE-Fly1.wav','audio/TIE/TIE-Fly2.wav',
		'audio/TIE/TIE-Fly3.wav','audio/TIE/TIE-Fly4.wav','audio/TIE/TIE-Fly5.wav','audio/TIE/TIE-Fly6.wav','audio/TIE/TIE-Fly7.wav']
		
		self.rotmatrix = viz.Matrix()
		
		self.trench = viz.addGroup()
		
		space = viz.add(viz.ENVIRONMENT_MAP,'Skybox/stars.jpg')
		skybox = viz.add('skydome.dlc')
		skybox.texture(space)
		m = viz.Matrix()
		m.postScale(100,100,100)
		skybox.setMatrix(m)
		
		self.model = None
		
		self.xWing = viz.add('x-wing/x-wing.dae')
		self.tie = viz.add('tie/tie.dae')
		
		self.destroyer = viz.add('StarDestroyer.dae')
		self.destroyer.setAxisAngle(0,1,0,-45)
		self.destroyer.setPosition(-1000, 250, 15000)
		
		self.destroyer2 = viz.add('StarDestroyer.dae')
		self.destroyer2.setAxisAngle(0,1,0,-45)
		self.destroyer2.setPosition(-1000, 500, 17500)
		
		self.deathStar = viz.add('DeathStar.dae')
		
		m = viz.Matrix()
		m.postScale(10, 10, 10)
		m.postAxisAngle(0,1,0,100)
		m.postTrans(1000,3000,20000)
		self.deathStar.setMatrix(m)
		self.deathStar.collideMesh()
		#self.deathStar.enable(viz.COLLIDE_NOTIFY)
		
		self.monCal = viz.add('MC80a.dae')
		self.monCal.setAxisAngle(0,1,0,45)
		self.monCal.setPosition(300, 500, 15000)
		
		self.picking = True
		self.win = False
		self.lose = False
		
		self.winSong = ''
		self.loseSong = ''
		self.ambient = ''
		
		self.pickShip()
		
	def onKeyDown(self, key):
		if self.win or self.lose:
			viz.quit()
		
		if not self.picking:
			if (key == viz.KEY_UP):
				#increase velocity
				self.scaleValue += .1
			elif (key == viz.KEY_DOWN):
				#decrease velocity
				self.scaleValue = self.scaleValue - .1 if self.scaleValue > 2 else 2
			elif key == 's':
				self.pitch += 5
				#incorporate +5 degree more pitch
				v = self.rotmatrix.preMultVec([1, 0, 0])
				self.rotmatrix.postAxisAngle(v[0], v[1], v[2], self.rotateValue if self.model.id == self.xWing.id else -self.rotateValue)
			elif key == 'w':
				self.pitch -= 5
				#incorporate -5 degree more pitch
				v = self.rotmatrix.preMultVec([1, 0, 0])
				self.rotmatrix.postAxisAngle( v[0], v[1], v[2], -self.rotateValue if self.model.id == self.xWing.id else self.rotateValue)
			elif key == 'd':
				self.roll -= 5
				#incorporate -5 degree more roll
				v = self.rotmatrix.preMultVec([0, 0, 1])
				self.rotmatrix.postAxisAngle( v[0], v[1], v[2], -self.rotateValue if self.model.id == self.xWing.id else self.rotateValue)
			elif key == 'a':
				self.roll += 5
				#incorporate +5 degree more roll
				v = self.rotmatrix.preMultVec([0, 0, 1])
				self.rotmatrix.postAxisAngle( v[0], v[1], v[2], self.rotateValue if self.model.id == self.xWing.id else -self.rotateValue)
			elif key == 'q':
				self.yaw -= 5
				#incorporate -5 degree more yaw
				v = self.rotmatrix.preMultVec([0, 1, 0])
				self.rotmatrix.postAxisAngle( v[0], v[1], v[2], -self.rotateValue)
			elif key == 'e':
				self.yaw += 5
				#incorporate +5 degree more yaw
				v = self.rotmatrix.preMultVec([0, 1, 0])
				self.rotmatrix.postAxisAngle( v[0], v[1], v[2], self.rotateValue)
			
			self.setOrientation()
		
	def onClick(self, click):
		if self.picking:
			choice = viz.pick(info = True)
			if choice.valid:
				if choice.object.id in [self.xWing.id, self.tie.id]:
					if choice.object.id == self.xWing.id:
						print("xwing")
						self.model = self.xWing
						self.tie.remove()
						
						self.winSong = 'audio/good-win.wav'
						self.loseSong = 'audio/good-fail.wav'
						
						self.ambient = viz.addAudio('audio/xWing-ambient.wav') 
						self.ambient.loop(viz.ON)
						self.ambient.play()
						
						self.picking = False
					elif choice.object.id == self.tie.id:
						print("tie")
						self.model = self.tie
						self.rotmatrix.postAxisAngle(0,1,0,180)
						self.xWing.remove()
						
						self.winSong = 'audio/bad-win.wav'
						self.loseSong = 'audio/bad-lose.wav'
						
						self.ambient = viz.addAudio('audio/tie-ambient.wav') 
						self.ambient.loop(viz.ON) 
						self.ambient.play()
						
						self.picking = False

					self.setOrientation() 
					self.setView() 
					
					self.trench = self.addTrench()
					self.trench.collideMesh()
					
					self.model.collideMesh()
					self.model.enable(viz.COLLIDE_NOTIFY)
					self.model.enable(viz.LIGHTING)
					
					self.starttimer(1, viz.FASTEST_EXPIRATION, viz.FOREVER)
					self.starttimer(3, 2, viz.FOREVER)

	def pickShip(self):
		self.picking = True
		
		m = viz.Matrix()
		m.postAxisAngle(0, 1, 0, 180)
		m.postTrans(-5, 0, 25)
		self.xWing.setMatrix(m)
		
		m = viz.Matrix()
		m.postTrans(5, 0, 25)
		self.tie.setMatrix(m)
		
	def setOrientation(self):
		m = self.rotmatrix.getMatrix()

		m.postTrans(self.x, self.y, self.z)

		self.model.setMatrix(m)
	
	def moveForward(self):
		v = self.rotmatrix.preMultVec([0, 0, 1]) if self.model.id != self.tie.id else self.rotmatrix.preMultVec([0, 0, -1])

		self.x += v[0] * self.scaleValue
		self.y += v[1] * self.scaleValue
		self.z += v[2] * self.scaleValue
		
		self.setOrientation()
		
	def setView(self):
		m = self.rotmatrix.getMatrix()
		
		v = []
		if self.model.id == self.tie.id:
			v = self.rotmatrix.preMultVec([0,0,-1])
			m.preAxisAngle(0,1,0,-180)
		else:
			v = self.rotmatrix.preMultVec([0,0,1])
			
		m.preTrans(0, 3, -10)
		
		t = [self.x - v[0]*15, self.y - v[1]*15, self.z - v[2]*15]
	
		m.postTrans(t)
		
		view = viz.MainView
		view.setMatrix(m)	
	
	def onTimer(self, num):
		if num == 1:
			self.moveForward()
			self.setView()
			self.t.remove()
			self.t = viz.addText("Lives: " + str(self.numLives), viz.SCREEN, pos = [0,0.9,0])
			self.t.font('Times New Roman')
			self.t.fontSize(20)
			
		if(num == 2):
			self.x, self.y, self.z = 0, 0, 0
			m = viz.Matrix()
			if self.model.id == self.tie.id:
				m.postAxisAngle(0, 1, 0, 180)
			self.rotmatrix = m
			self.model.visible(viz.ON)
			
		if num == 3:
			self.chooseSound()
		
		
			
	def onCollide(self, obj):
		if obj.obj1 == self.deathStar or obj.obj2 == self.deathStar:
			viz.playSound('audio/explosion.wav')
			self.winGame()
			return
		self.numLives -= 1
		if self.numLives == 0:
			self.endGame()
		self.model.visible(viz.OFF)
		viz.playSound('audio/explosion.wav')
		self.starttimer(2,1,0)
		print("Collision!")
		
		
		
	def endGame(self):
		viz.MainWindow.setScene(viz.Scene3)
		self.lose = True
		self.killtimer(1)
		self.killtimer(2)
		self.killtimer(3)
		self.ambient.stop()
		self.model.remove()
		viz.playSound(self.loseSong)
		print "You Lose!"
		
	def winGame(self):
		viz.MainWindow.setScene(viz.Scene2)
		self.win = True
		self.killtimer(1)
		self.killtimer(2)
		self.killtimer(3)
		self.model.remove()
		self.ambient.stop()
		self.model.remove()
		viz.playSound(self.winSong)
			
	def addTrench(self):
		trench = viz.addGroup()
		
		leftWall = vizshape.addBox(size = [200, 200, 20000])
		rightWall = vizshape.addBox(size = [200, 200, 20000])
		floor = vizshape.addBox(size = [200, 2, 20000])
		ceiling = vizshape.addBox(size = [200, 2, 20000])
		
		m = viz.Matrix()
		m.postTrans(-200, 50, 2500)		
		leftWall.setMatrix(m)
		
		m = viz.Matrix()
		m.postTrans(200, 50, 2500)
		rightWall.setMatrix(m)
		
		m = viz.Matrix()
		m.postTrans(0, -50, 2500)
		floor.setMatrix(m)
		
		m = viz.Matrix()
		m.postTrans(0, 125, 2000)
		ceiling.setMatrix(m)
		
		trenchTex = viz.addTexture('trench2.jpg')
		leftWall.texture(trenchTex)
		rightWall.texture(trenchTex)
		floor.texture(trenchTex)
		
		ceiling.visible(viz.OFF)
		
		leftWall.setParent(trench)
		rightWall.setParent(trench)
		floor.setParent(trench)
		ceiling.setParent(trench)
		
		obs1 = vizshape.addBox(size = [400, 175, 50])
		obs1.setPosition(0, 60, 650)
		obs1.texture(trenchTex)
		obs1.setParent(trench)
		
		obs2 = vizshape.addBox(size = [250, 150, 50])
		obs2.setPosition(-60, 0, 750)
		obs2.texture(trenchTex)
		obs2.setParent(trench)
		
		obs3 = vizshape.addBox(size = [400, 125, 50])
		obs3.setPosition(0, -60, 950)
		obs3.texture(trenchTex)
		obs3.setParent(trench)
		
		obs4_1 = vizshape.addBox(size = [400, 100, 50])
		obs4_1.setPosition(0, 100, 1100)
		obs4_1.texture(trenchTex)
		obs4_1.setParent(trench)
		
		obs4_2 = vizshape.addBox(size = [400, 75, 50])
		obs4_2.setPosition(0, -10, 1100)
		obs4_2.texture(trenchTex)
		obs4_2.setParent(trench)
		
		obs5_1 = vizshape.addBox(size = [75, 200, 1000])
		obs5_1.setPosition(50, 0, 2000)
		obs5_1.texture(trenchTex)
		obs5_1.setParent(trench)
		
		obs5_2 = vizshape.addBox(size = [75, 200, 1000])
		obs5_2.setPosition(-50, 0, 2000)
		obs5_2.texture(trenchTex)
		obs5_2.setParent(trench)
		
		obs6_1 = vizshape.addBox(size = [400, 100, 1000])
		obs6_1.setPosition(0, 100, 3000)
		obs6_1.texture(trenchTex)
		obs6_1.setParent(trench)
		
		obs6_2 = vizshape.addBox(size = [400, 50, 1000])
		obs6_2.setPosition(0, -10, 3000)
		obs6_2.texture(trenchTex)
		obs6_2.setParent(trench)
		
		obs7_1 = vizshape.addBox(size = [75, 200, 1000])
		obs7_1.setPosition(50, 0, 4000)
		obs7_1.texture(trenchTex)
		obs7_1.setParent(trench)
		
		obs7_2 = vizshape.addBox(size = [75, 200, 1000])
		obs7_2.setPosition(-50, 0, 4000)
		obs7_2.texture(trenchTex)
		obs7_2.setParent(trench)
		
		obs8_1 = vizshape.addBox(size = [400, 100, 1000])
		obs8_1.setPosition(0, 100, 5000)
		obs8_1.texture(trenchTex)
		obs8_1.setParent(trench)
		
		obs8_2 = vizshape.addBox(size = [400, 50, 1000])
		obs8_2.setPosition(0, -10, 5000)
		obs8_2.texture(trenchTex)
		obs8_2.setParent(trench)
		
		obs9 = vizshape.addBox(size = [200, 200, 1000])
		obs9.setPosition(-50, 0, 6000)
		obs9.texture(trenchTex)
		obs9.setParent(trench)
		
		obs10 = vizshape.addBox(size = [200, 200, 1000])
		obs10.setPosition(0, 100, 7000)
		obs10.texture(trenchTex)
		obs10.setParent(trench)
		
		obs11 = vizshape.addBox(size = [200, 200, 1000])
		obs11.setPosition(50, 0, 8000)
		obs11.texture(trenchTex)
		obs11.setParent(trench)
		
		obs12_1 = vizshape.addBox(size = [200, 200, 1000])
		obs12_1.setPosition(0, -100, 9000)
		obs12_1.texture(trenchTex)
		obs12_1.setParent(trench)
		
		obs12_2 = vizshape.addBox(size = [200, 100, 1000])
		obs12_2.setPosition(0, 100, 9000)
		obs12_2.texture(trenchTex)
		obs12_2.setParent(trench)
		
		obs13_1 = vizshape.addBox(size = [200, 200, 1000])
		obs13_1.setPosition(0, -100, 10000)
		obs13_1.texture(trenchTex)
		obs13_1.setParent(trench)
		
		obs13_2 = vizshape.addBox(size = [150, 100, 1000])
		obs13_2.setPosition(50, 50, 10000)
		obs13_2.texture(trenchTex)
		obs13_2.setParent(trench)
		
		obs13_1 = vizshape.addBox(size = [200, 200, 1000])
		obs13_1.setPosition(0, -100, 11000)
		obs13_1.texture(trenchTex)
		obs13_1.setParent(trench)
		
		obs13_2 = vizshape.addBox(size = [150, 100, 1000])
		obs13_2.setPosition(60, 50, 11000)
		obs13_2.texture(trenchTex)
		obs13_2.setParent(trench)
		
		obs13_3 = vizshape.addBox(size = [200, 100, 1000])
		obs13_3.setPosition(0, 100, 11000)
		obs13_3.texture(trenchTex)
		obs13_3.setParent(trench)
		
		
		return trench
		
	def chooseSound(self):
		temp = random.randint(0,4)
		temp2 = random.randint(5,11)
		
		if(self.model.id == self.xWing.id):
			sound = viz.addAudio(self.sounds[temp] ) 
			sound.volume(.5)
			sound.play()
		else:
			sound = viz.addAudio(self.sounds[temp2])
			sound.volume(.5)
			sound.play()
		