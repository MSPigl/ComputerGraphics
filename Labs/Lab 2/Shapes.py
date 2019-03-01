import math
class Circle:
	def __init__(self,rad):
		self.radius = rad
		
	def area(self):
		return math.pi * self.radius *self.radius
		
	def perimeter(self):
		return 2*math.pi*self.radius
		
	def toString(self):
		return("Circle with radius {}".format(self.radius))
		
class Rectangle:
	def __init__(self, w, h):
		self.width = w
		self.height = h
		
	def area(self):
		return self.width * self.height
		
	def perimeter(self):
		return 2*self.width + 2*self.height
		
	def toString(self):
		return("Rectangle with width {} and height {}".format(self.width, self.height))