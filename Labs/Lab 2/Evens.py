def evens(arr):
	newList = []
	
	for elm in arr:
		if elm % 2 == 0:
			newList.append(elm)
	return newList

print(evens([3,9,4,5,2,8,9,2]))
print(evens([6,6,3,12,5]))
print(evens([3,5,9]))