class AVL(object):

	def __init__(self):
		self.root = None

	def find(self, x):
		return self.root and self.root.find(x)

	def min(self):
		return self.root and self.root.min()

	def insert(self, key, value):
		if self.root is None:
			node = AVLNode(key, value)
			self.root = node
		else:
			node = self.find(key)
			if node is not None:
				node.append(value)
			else:
				new_node = AVLNode(key, value)
				self.root.insert(new_node)
				node = new_node

		# avl augmentation
		node.update_subtree_info()
		self.rebalance(node)

		return node

	def delete(self, key, value):
		node = self.find(key)
		deleted = None
		if node is None:
			deleted = None
			return deleted
		elif node is not None and len(node.value) == 1:
			if node is self.root:
				pseudo_root = AVLNode(None, None)
				pseudo_root.left = self.root
				self.root.parent = pseudo_root
				deleted_node = self.root.delete()
				self.root = pseudo_root.left
				if self.root is not None:
					self.root.parent = None
				deleted = deleted_node
			else:
				deleted = node.delete()

			self.rebalance(deleted.parent)
			return deleted
		elif node is not None and len(node.value) > 1:
			node.value.remove(value)
			return None

	def successor(self, key):
		node = self.find(key)
		return node and node.successor()

	def check_ri(self, node):
		if self.root is not None:
			if self.root.parent is not None:
				raise RuntimeError("BST RI violated by the root node's parent pointer")
			self.root.check_ri()

	def rebalance(self, node):
		while node is not None:
			node.update_subtree_info()

			if AVL._height(node.left) >= 2 + AVL._height(node.right):
				if AVL._height(node.left.left) < AVL._height(node.left.right):
					self.left_rotate(node.left)
				self.right_rotate(node)
			elif AVL._height(node.right) >= 2 + AVL._height(node.left):
				if AVL._height(node.right.right) < AVL._height(node.right.left):
					self.right_rotate(node.right)
				self.left_rotate(node)
			node = node.parent

	@staticmethod
	def _height(node):
		if node is not None:
			return node.height
		else:
			return -1

	def left_rotate(self, x):
		y = x.right
		y.parent = x.parent
		if y.parent is None:
			self.root = y
		else:
			if x.parent.left is x:
				y.parent.left = y
			else:
				y.parent.right = y
		x.right = y.left
		if x.right is not None:
			x.right.parent = x
		x.parent = y
		y.left = x
		x.update_subtree_info()
		y.update_subtree_info()

	def right_rotate(self, x):
		y = x.left
		y.parent = x.parent
		if y.parent is None:
			self.root = y
		else:
			if x.parent.right is x:
				y.parent.right = y
			else:
				y.parent.left = y
		x.left = y.right
		if x.left is not None:
			x.left.parent = x
		x.parent = y
		y.right = x
		x.update_subtree_info()
		y.update_subtree_info()

	def rank(self, key):
		if self.root is not None:
			return self.root.rank(key)
		return 0

	def lca(self, low_key, high_key):
		return self.root and self.root.lca(low_key, high_key)

	def list(self, low_key, high_key):
		result = []
		lca = self.lca(low_key, high_key)
		if lca is not None:
			lca.list(low_key, high_key, result)
		return result

class AVLNode(object):

	def __init__(self, key, value):
		self.key = key
		self.value = []
		self.parent = None
		self.left = None
		self.right = None
		self.height = 0
		self.tree_size = 1

		self.value.append(value)

	def find(self, key):
		if key < self.key:
			return self.left and self.left.find(key)
		elif key > self.key:
			return self.right and self.right.find(key)
		return self

	def min(self):
		if self.left is None:
			return self
		else:
			return self.left.min()

	def max(self):
		if self.right is None:
			return self
		else:
			return self.right.max()

	def successor(self):
		if self.right is not None:
			return self.right.min()
		current = self
		while current.parent is not None and current is current.parent.right:
			current = current.parent
		return current.parent

	def append(self, value):
		self.value.append(value)
		self.update_subtree_info()

	def insert(self, node):
		# inserts node into tree rooted at self
		if node.key < self.key:
			if self.left is None:
				self.left = node
				node.parent = self
			else:
				self.left.insert(node)
		elif node.key > self.key:
			if self.right is None:
				self.right = node
				node.parent = self
			else:
				self.right.insert(node)
				node.update_subtree_info()
		else:
			return self

	def delete(self):
		# deletes node from tree. idea: find successor and switch pointers
		left_parent = self is self.parent.right
		if self.right is None and self.left is None:
			if left_parent:
				self.parent.right = None
			else:
				self.parent.left = None
			return self
		elif self.right is None and self.left is not None:
			if left_parent:
				self.parent.right, self.left.parent = self.left, self.parent
			else:
				self.parent.left, self.left.parent = self.left, self.parent
			return self
		elif self.right is not None and self.left is None:
			if left_parent:
				self.parent.right, self.right.parent = self.right, self.parent
			else:
				self.parent.left, self.right.parent = self.right, self.parent
			return self
		else:
			s = self.successor()
			deleted_node = s.delete()
			self.key, s.key, self.value, s.value = s.key, self.key, s.value, self.value
			return deleted_node

	def check_ri(self):
		# rep invariant for BST: keys smaller and pointers match
		test_left_key = False
		test_left_parent = False
		test_right_key = False
		test_right_parent = False
		if self.left is not None:
			test_left_key = self.left.key <= self.key
			test_left_parent = self.left.parent is self
		if self.right is not None:
			test_right_key = self.key <= self.right.key
			test_right_parent = self.right.parent is self
		bst_test = test_left_key and test_right_key and test_left_parent and test_right_parent

		# extension for AVL
		difference = abs(AVL._height(self.left) - AVL._height(self.right))
		avl_test = difference <= 1

		# extension for range tree
		rt_test = self.tree_size == self.uncached_tree_size()

		return bst_test and avl_test and rt_test

	def update_subtree_info(self):
		self.height = self.uncached_height()
		self.tree_size = self.uncached_tree_size()

	def uncached_height(self):
		left_height = self.left.height if self.left is not None else -1
		right_height = self.right.height if self.right is not None else -1
		return 1 + max(left_height, right_height)

	def uncached_tree_size(self):
		return 1 + (((self.left and self.left.tree_size) or 0) + ((self.right and self.right.tree_size) or 0))

	def rank(self, key):
		# number of keys <= the given key in subtree rooted at this node
		if key < self.key:
			if self.left is not None:
				return self.left.rank(key)
			else:
				return 0
		if self.left:
			lrank = len(self.value) + self.left.tree_size
		else:
			lrank = len(self.value)
		if key > self.key and self.right is not None:
			return lrank + self.right.rank(key)
		return lrank

	def lca(self, low_key, high_key):
		if low_key <= self.key <= high_key:
			return self
		if low_key < self.key:
			return self.left and self.left.lca(low_key, high_key)
		else:
			return self.right and self.right.lca(low_key, high_key)
		pass

	def list(self, low_key, high_key, result):
		if self.key >= low_key and self.left is not None:
			self.left.list(low_key, high_key, result)
		if self.key <= high_key and self.right is not None:
			self.right.list(low_key, high_key, result)
		if low_key <= self.key <= high_key:
			result.append(self)


import random
if __name__ == '__main__':

	a = AVL()
	value_list = []

	for i in range(1,20):
		value_list.append(random.randint(1,100))

	value_list = [99, 58, 74, 44, 70, 12, 19, 36, 15, 4, 94, 58, 85, 5, 62, 28, 5, 73, 48]
	print(value_list)

	for v in value_list:
		a.insert(v, random.randint(1,10))

		result = a.list(min(value_list), max(value_list))

		def print_tree(node):
			output = ""
			n = node
			if n is not None:
				output += "Key: " + str(n.key) + " "
				output += "TreeHeight: " + str(n.height) + " "
				if n.left is not None:
					output += "Left:" + str(n.left.key) + "  "
				else:
					output += "Left:    "
				if n.right is not None:
					output += "Right: " + str(n.right.key) + " "
				else:
					output += "Right:    "
				if n.parent is not None:
					output += "Parent: " + str(n.parent.key) + " "
				else:
					output += "Parent:    "
			print(output)

		for r in result:
			print_tree(r)
		print("")
		print("")
		print("")
