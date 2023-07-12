class MinHeap(object):

	def __init__(self):
		self.heap = []
		self.root = None

	def append(self, x):

		if len(self.heap) == 0:
			self.heap.append(x)

		else:
			# find appropriate place in heap
			insertion_point = len(self.heap)
			self.heap.append(x)
			while True:
				parent_index = insertion_point // 2
				parent = self.heap[parent_index]
				if x >= parent or parent is None:
					break
				self.heap[insertion_point] = parent
				self.heap[parent_index] = x
				insertion_point = insertion_point // 2

	def delete(self, x):
		pass


if __name__ == "__main__":

	mh = MinHeap()

	elements = [1,3,2,4,5,6,7,8,9,10,11,12,13,14,15,0]

	for e in elements:
		mh.append(e)
		print(mh.heap)

	print(mh.heap)
