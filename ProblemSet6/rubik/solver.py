import rubik
from Queue import Queue

def BFS_Head(s, depth):
	level = {s: 0}
	parent = {s: None}
	i = 1
	frontier = Queue()
	frontier.put(s)
	while not frontier.empty() and i < depth:
		next = []
		while not frontier.empty():
			u = frontier.get()
			adjacent_states = []
			for adj in rubik.quarter_twists:
				perm = rubik.perm_apply(adj,u)
				perm_name = rubik.quarter_twists_names[adj]
				adjacent_states.append((perm, perm_name, adj))

			for v in adjacent_states:
				if v[0] not in level:
					level[v[0]] = i
					parent[v[0]] = (u,v[2])
					next.append(v[0])

		for n in next:
			frontier.put(n)
		i += 1

	return parent

def BFS_Tail(s, head_dict, depth):
	if head_dict is None:
		return None
	level = {s: 0}
	parent = {s: None}
	head_dict = head_dict
	joined_dict = {}
	i = 1
	frontier = Queue()
	frontier.put(s)
	while not frontier.empty() and i < depth:
		next = []
		while not frontier.empty():
			u = frontier.get()
			adjacent_states = []
			for adj in rubik.quarter_twists:
				perm = rubik.perm_apply(adj,u)
				perm_name = rubik.quarter_twists_names[adj]
				adjacent_states.append((perm, perm_name, adj))

			for v in adjacent_states:
				if v[0] not in level:
					level[v[0]] = i
					parent[v[0]] = (u,v[2])
					next.append(v[0])
					if i == depth-1:
						for adj in rubik.quarter_twists:
							if rubik.perm_apply(adj, v[0]) in head_dict:
								joined_dict[rubik.perm_apply(adj, v[0])] = (v[0], adj)

		for n in next:
			frontier.put(n)
		i += 1

	return parent, joined_dict

def shortest_path(start, end):
	"""
	Using 2-way BFS, finds the shortest path from start_position to
	end_position. Returns a list of moves.

	You can use the rubik.quarter_twists move set.
	Each move can be applied using rubik.perm_apply
	"""

	start_parents = None
	depth = 8

	try:
		start_parents = BFS_Head(start, depth)
		x = start_parents[end]
		ans = []
		current = end
		while start_parents[current] is not None:
			ans.append(start_parents[current][1])
			current = start_parents[current][0]
		ans.reverse()
	except:
		try:
			# answer not in first half, continue searching
			end_parents, joined_dict = BFS_Tail(end, start_parents, depth - 1)

			ans = []
			v = joined_dict.keys()[0]
			u,adj = joined_dict[v]

			# build answer from head leaf upwards, then reverse
			current = v
			while start_parents[current] is not None:
				ans.append(start_parents[current][1])
				current = start_parents[current][0]
			ans.reverse()

			# append arbritrarily chosen midpoint to answer
			ans.append(rubik.perm_inverse(adj))

			# build answer from tail leaf up
			current = u
			while end_parents[current] is not None:
				ans.append(rubik.perm_inverse(end_parents[current][1]))
				current = end_parents[current][0]

		except:
			ans = None

	return ans
