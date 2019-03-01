def shortWords(arr):
	newList = []
	
	for elm in arr:
		if len(elm) <= 2:
			newList.append(elm)
	return newList
	
print(shortWords(["I", "python", "to", "or", "candy", "as"]))
print(shortWords(["wonder", "to", "beach", "me"]))
print(shortWords(["toolong", "waytoolong"]))