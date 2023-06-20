from dnaseq import subsequenceHashes

if __name__ == '__main__':

	t = 'this is a long string with all kinds of stuff inside it'

	it = iter(t)

	i = subsequenceHashes(it, 3)

	for x in i:
		print(x)

	print(type(i))

