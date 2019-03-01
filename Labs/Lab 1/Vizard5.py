n = input("please enter an integer -->")
isPrime = True

for i in range (2, n):
	if (n % i) == 0:
		print(str(n) + " is not a prime number")
		isPrime = False
		break

if isPrime:
	print(str(n) + " is a prime number")