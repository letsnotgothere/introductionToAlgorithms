
from big_num import BigNum

if __name__ == '__main__':

	onetwothreefour = "4D2"
	fivesixseveneight = "162E"

	bn_1234 = BigNum.from_hex(onetwothreefour)
	bn_5678 = BigNum.from_hex(fivesixseveneight)

	result = bn_1234 * bn_5678

	print(bn_1234.__dict__)
	print(bn_5678.__dict__)
	print(result.__dict__)