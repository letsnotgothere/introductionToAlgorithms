#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *
import datetime

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
	# Initializes a new multi-value dictionary, and adds any key-value
	# 2-tuples in the iterable sequence pairs to the data structure.
	def __init__(self, pairs=[]):
		self.dict = {}
		for p in pairs:
			self.put(p[2],(p[0],p[1]))
	# Associates the value v with the key k.

	def put(self, k, v):
		if k not in self.dict.keys():
			self.dict[k] = [v]
		else:
			self.dict[k].append(v)

	# Gets any values that have been associated with the key k; or, if
	# none have been, returns an empty sequence.
	def get(self, k):
		try:
			return self.dict[k]
		except KeyError:
			return []

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
	window = ''
	index = 0

	for i in range(k):
		window += seq.next()
		index += 1
	r = RollingHash(window)

	yield index-k, window, r.current_hash()

	for i in seq:
		r.slide(window[0], i)
		window = window[1:] + i
		index += 1
		yield index-k, window, r.current_hash()


# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)

def intervalSubsequenceHashes(seq, k, m):
	assert m>= k
	try:
		index = 0
		while True:
			window = ''
			for i in range(0,k):
				window += seq.next()
			r = RollingHash(window)
			yield index, window, r.current_hash()
			for x in range(0,m-k):
				seq.next()
			index += m
	except StopIteration:
		return

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
	start_time = datetime.datetime.now().time()
	print('Building Hash Table for Subsequence A...')
	a_dict = Multidict(intervalSubsequenceHashes(a,k,m))
	print('Hash Table Built')
	for b_index, b_window, b_hash in subsequenceHashes(b,k):
		for a_index, a_window in a_dict.get(b_hash):
			if a_window == b_window:
				yield a_index,b_index
	end_time = datetime.datetime.now().time()
	print('Start Time: ', str(start_time))
	print('End Time: ', str(end_time))


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
		sys.exit(1)

	# The arguments are, in order: 1) Your getExactSubmatches
	# function, 2) the filename to which the image should be written,
	# 3) a tuple giving the width and height of the image, 4) the
	# filename of sequence A, 5) the filename of sequence B, 6) k, the
	# subsequence size, and 7) m, the sampling interval for sequence
	# A.
	compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
