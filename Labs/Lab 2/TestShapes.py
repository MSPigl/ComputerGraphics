from Shapes import *

c1 = Circle(5)
r1 = Rectangle(3,2)
c2 = Circle(3)
c3 = Circle(1)
r2 = Rectangle(1,1)

listShapes = [c1,r1,c2,c3,r2]

for i in listShapes:
	print(i.toString())
	print("Area: " + str(i.area()))
	print("Perimeter: " + str(i.perimeter()))