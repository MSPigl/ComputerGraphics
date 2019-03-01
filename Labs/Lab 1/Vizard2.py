years = input("Enter number of years -->")
months = input("Enter number of months -->")
months = months + (years * 12)
seconds = months * 30 * 24 * 360
print("You are " + str(seconds) + " seconds old.")