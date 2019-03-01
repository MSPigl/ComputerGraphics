def amount(meal, tax = .07, tip = .15):
	return int(meal + (meal * tax) + (meal * tip))
	
#print(amount(100))
#print(amount(100, 0.03, .20))
#print(amount(100, tip = .10))
#print(amount(100, tax = 0.05))
#print(amount(100, tip = 0.12, tax = 0.04))
#print(amount(100, tax = 0.04, 0.10)) <-- Intentional ERROR

def perfect(number):
	divisors = []
	
	for i in range (1, number):
		if number % i == 0:
			divisors.append(i)
	
	sum = 0
	for i in range(0, len(divisors)):
		sum += divisors[i]
	
	if sum == number:
		return True
	
	return False
	
print(perfect(6))
print(perfect(8128))
print(perfect(68))
print(perfect(28))
	
	
	