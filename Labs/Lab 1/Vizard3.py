dollars = input("Enter a dollar amount -->")

twenties = dollars / 20
dollars = dollars % 20

tens = dollars / 10
dollars = dollars % 10

fives = dollars / 5
dollars = dollars % 5

ones = dollars

print(str(twenties) + " twenties")
print(str(tens) + " tens")
print(str(fives) + " fives")
print(str(ones) + " ones")
	
	
	