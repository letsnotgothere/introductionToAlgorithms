import os


class KaratsubaMultiplication(object):

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.answer = self.karatsuba2(x,y)

	def karatsuba2(self,x, y):
		"""Function to multiply 2 numbers in a more efficient manner than the grade school algorithm"""
		if len(str(x)) == 1 or len(str(y)) == 1:
			return x * y
		else:
			n = max(len(str(x)), len(str(y)))
			nby2 = n / 2

			a = x / 10 ** (nby2)
			b = x % 10 ** (nby2)
			c = y / 10 ** (nby2)
			d = y % 10 ** (nby2)

			ac = self.karatsuba2(a, c)
			bd = self.karatsuba2(b, d)
			ad_plus_bc = self.karatsuba2(a + b, c + d) - ac - bd

			# this little trick, writing n as 2*nby2 takes care of both even and odd n
			prod = ac * 10 ** (2 * nby2) + (ad_plus_bc * 10 ** nby2) + bd

			return prod

	def karatsuba(self,x,y):

		'''
		assumes values passed in as string of length 2^d where d > 1
		of which all can be cast correctly as ints
		won't go into handling odd or unequal lengths

		steps:
			1- get digit length of x, y
			2- calculate a,b,c,d
			3 - recursively calculate ac
			4 - recursively calculate bd
			5 - recursively calculate (a+b)(c+d)
			6 - (5) - ((3) + (4)) to get (ad + bc)
			7 - return 10^n ac + 10^n/2 ad+bc + bd
		'''

		n = len(x)


		a,b = x[:n/2],x[n/2:]
		c,d = y[:n/2],y[n/2:]

		if n > 2:
			ac = self.karatsuba(a,c)
			if ac != int(a)*int(c):
				print("AC error")
			bd = self.karatsuba(b,d)
			if bd != int(b)*int(d):
				print("BD error")
			aplusb_x_cplusd = self.karatsuba(str(int(a)+int(b)),str(int(c)+int(d)))

			ad_plus_bc = aplusb_x_cplusd - ac - bd
			answer = (pow(10,n) * ac) + (pow(10,n/2) * ad_plus_bc) + bd
			return answer
		else:
			return int(x)*int(y)

	def get_answer(self):
		return self.answer


if __name__ == "__main__":

	x = 123
	y = 45
	k = KaratsubaMultiplication(x,y)
	ans = k.get_answer()
	print(ans)
