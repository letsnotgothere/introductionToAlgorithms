
from big_num import BigNum

if __name__ == '__main__':

	numerator = "BC614E"
	#numerator = "9A0300"
	divisor = "04D2"

	n = BigNum.from_hex(numerator)
	d = BigNum.from_hex(divisor)

	div = n // d
	mod = n % d

	print("")
	print("Numerator", n.__dict__)
	print("Divisor",d.__dict__)
	print("Quotient", div.__dict__)
	print("Modulus", mod.__dict__)