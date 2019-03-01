def boggle(arr):
	score = 0
	
	for element in range(0, len(arr)):
		if len(arr[element]) <= 4:
			score += 1
		elif len(arr[element]) == 5:
			score += 2
		elif len(arr[element]) == 6:
			score += 3
		elif len(arr[element]) == 7:
			score += 5
		else:
			score += 11
	
	return score

print(boggle(["cat", "tea", "mate", "computer", "ale", "bat"]))
print(boggle(["honest", "yelps", "yelp", "python", "pythons"]))