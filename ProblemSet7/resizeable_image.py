import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
	def best_seam(self):
		coords = []

		h = self.height - 1
		w = self.width - 1

		# energy function takes pixels 0... w-1, 0... h-1

		# of all possible seams, we want the one with the minimum energy
		# subproblems: suffixes dp[i:] -> O(N)
		# guesses: choose next pixel below (left, centre, right) -> O(1)
		# recurrence: dp[i,j] = min(dp[i+1,j-1],dp[i+1,j],dp[i+1,j+1]) + energy(i,j)
		# top. order: no cycles
		# original solution: for x in range(0,w-1): min(dp[x,0])

		dp = {}

		# set initial bottom layer, cleaner
		for i in range(0,w+1):
			dp[(i,h)] = self.energy(i,h)

		# build dp table bottom up
		for j in range(h - 1, -1, -1):
			for i in range(0,w+1):
				energy = self.energy(i,j)

				if i == 0:
					dp[(i,j)] = min(dp[i,j+1],dp[i+1,j+1]) + energy
				elif i == w:
					dp[(i, j)] = min(dp[i-1,j+1],dp[i,j+1]) + energy
				else:
					dp[(i, j)] = min(dp[i-1,j+1],dp[i,j+1],dp[i+1,j+1]) + energy

		# find best seam
		min_i = None
		min_seen = None
		for i in range(0,w):
			if min_seen is None or min_seen > dp[(i,0)]:
				min_seen = dp[(i,0)]
				min_i = i

		# follow best seam
		i = min_i
		coords.append((min_i,0))
		for j in range(1,h+1):
			# indexes: c,l,r
			choices = [(dp[i,j],0), None, None]
			if i != 0:
				choices[1] = (dp[i-1,j],-1)
			if i != w:
				choices[2] = (dp[i+1,j],+1)

			choice = min(c for c in choices if c is not None)

			coords.append((i + choice[1],j))
			i += choice[1]

		return coords

	def remove_best_seam(self):
		self.remove_seam(self.best_seam())
