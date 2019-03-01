import random
# Author: R. Flatland
# Generates random terrain using diamond-square algorithm

# Input: a 2D array called terrain and a row and column (r,c) 
# Returns: If (r,c) is a valid location in terrain, then it returns the value
# stored at that location and a 1.  Otherwise it returns a 0 and a
# 0.
def getVal(terrain,r,c):
	if r < 0 or c < 0 or r >= len(terrain) or c >= len(terrain[0]):
		return 0,0
	else:
		return terrain[r][c],1

# Input: an integer k that determines the size of the terrain.
# Returns: Generates an array of size 2^k+1 x 2^k+1 of random 
# elevation data using the diamond-square algorithm.
def diamondSquare(k):
	# size of the 2D array
	size = pow(2,k)+1
	
	# create a 2D array of the proper size, initialized to -1
	terrain =[[-1 for row in range(0,size)] for col in range(0,size)]

	# initialize the four corner elevations of terrain
	terrain[0][0] = 2
	terrain[0][size-1] = 0
	terrain[size-1][0] = 1
	terrain[size-1][size-1] = .1
	
	# Random amount added to each elevation is selected from this range
	rndRange = [0,1]
	# Note - size is initially set to the number of rows/columns in the 
	# terrain array, which is also the size of the largest square in the
	# diamond-square algorithm.  In each iteration of the algorithm, the
	# size of the squares & diamonds decreases by a factor of 1/2, and so
	# does the value of the size variable. 
	for i in range(0,k):
		# fill in center of each square to create diamonds
		for r in range(size/2,len(terrain),size):
			for c in range(size/2,len(terrain),size):
				# compute average of square's four corner elevations
				v1,c1 = getVal(terrain,r-size/2,c-size/2)
				v2,c2 = getVal(terrain,r-size/2,c+size/2)
				v3,c3 = getVal(terrain,r+size/2,c-size/2)
				v4,c4 = getVal(terrain,r+size/2,c+size/2)
				terrain[r][c] = (v1 + v2 + v3 + v4)/(c1 + c2 + c3 + c4) + \
								random.randint(rndRange[0],rndRange[1])/10.0
				
				
		# fill in center of each diamond to create squares
		for r in range(0,len(terrain),size/2):
			for c in range(0,len(terrain),size/2):
				if terrain[r][c] == -1:
					# compute average of diamonds's four corner elevations
					v1,c1 = getVal(terrain,r,c-size/2)
					v2,c2 = getVal(terrain,r,c+size/2)
					v3,c3 = getVal(terrain,r+size/2,c)
					v4,c4 = getVal(terrain,r-size/2,c)
					terrain[r][c] = (v1 + v2 + v3 + v4)/(c1 + c2 + c3 + c4) + \
									random.randint(rndRange[0],rndRange[1])/10
					
		# size of squares/diamonds is cut in half			
		size = size/2
		
		
	return terrain
			