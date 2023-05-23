class RollingHash(object):

	def __init__(self):

		self.base = 256
		self.p = self.calculate_p()
		self.hash = 0
		self.letters = []

		# this is base^windowsize mod p, however needs recomputing op since window size changes
		self.magic = 1

		# multiplicative inverse of base mod p
		self.ibase = pow(self.base,self.p-2,self.p) % self.p

	def calculate_p(self):
		return self.getPrime(self.base**3)

	def isPrime(self, X):
		for i in range(2, int(X**0.5) + 1, 1):
			if X % i == 0:
				# Factor found
				return False
		return True

	def getPrime(self, n):
			current = n+1
			while True:
				if self.isPrime(current):
					return current
				current += 1

	def append(self, c):
		self.letters.append(c)
		self.hash = ((self.hash * self.base) + ord(c)) % self.p
		self.magic = (self.magic * self.base) % self.p

	def skip(self, c):
		del self.letters[0]
		self.magic = (self.magic * (self.ibase % self.p)) % self.p
		self.hash = (self.hash - (ord(c) * self.magic) + (self.p * self.base)) % self.p

	def get_hash(self):
		return self.hash

	def get_window(self):
		return self.letters


if __name__ == '__main__':

	def log_output(rh, op):
		print('Operation: ' + op, 'Hash: ' + str(rh.hash), 'Ibase: ' + str(rh.ibase), 'Magic: ' + str(rh.magic), rh.get_window())

	s = 'elf'
	t = 'the awesome story that was unexplainable was that of the elf and the cart'

	rs = RollingHash()
	rt = RollingHash()
	rf = RollingHash()

	for i in range(len(s)):
		rs.append(s[i])
		log_output(rt, 'pre-a')
		rt.append(t[i])
		log_output(rt, 'pos-a')

	print(rt.p)
	print('')
	print('')
	log_output(rs, '-')
	log_output(rt, '-')
	log_output(rf, '-')

	print('')
	print('')


	for i in range(len(s),len(t)):
		rt.append(t[i])
		rt.skip(t[i-len(s)])
		if rs.get_hash() == rt.get_hash():
			print(rt.get_window())