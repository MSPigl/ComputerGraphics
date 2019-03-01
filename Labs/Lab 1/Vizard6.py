p = input("Enter a perimeter -->")

numTri = 0
for i in range (1,p):
	for j in range (1,p-i):
		k = p - i - j
		if((i+j) > k) and ((i+k) > j) and ((j+k) > i):
			if(i <= j and j <= k):
				numTri += 1
			
print(numTri)
				