from Queue import PriorityQueue

class Graph:

	def __init__(self):
		self.vertices = {}
		self.edges = {}

	def add_vertex(self, x):
		self.vertices[x] = True
		self.edges[x] = []

	def add_edge(self, u, v, w):
		if (v,w) not in self.edges[u]:
			self.edges[u].append((v, w))
		if (u,w) not in self.edges[v]:
			self.edges[v].append((u, w))

	def adjacency(self,x):
		return self.edges[x]

	def get_vertices(self):
		return self.vertices
	
	def get_edges(self):
		return self.edges

	def DFS(self, s):
		parents = {}
		time_visited = {}
		edge_classifier = {}
		visited = []
		for v in sorted(self.vertices):
			if v not in parents:
				parents[v] = None
				time_visited[v] = 0
				self.DFS_Visit(parents, visited, time_visited, edge_classifier, v)
				visited.append(v)
		return parents, visited, time_visited, edge_classifier

	def DFS_Visit(self, parents, visited, time_visited, edge_classifier, s):
		for v in sorted(self.adjacency(s)):
			if v[0] not in parents:
				edge_classifier["Forest"] = True
				parents[v[0]] = s
				time_visited[v[0]] = time_visited[s] + 1
				self.DFS_Visit(parents, visited, time_visited, edge_classifier, v[0])
				visited.append(v[0])
			else:
				if time_visited[v[0]] < time_visited[s]:
					edge_classifier["Backwards"] = True
				elif time_visited[v[0]] > time_visited[s]:
					edge_classifier["Forward"] = True
				else:
					edge_classifier["Cross"] = True

	def BFS(self, s):
		level = {s: 0}
		parent = {s: None}
		i = 1
		frontier = [s]
		while frontier:
			next = []
			for u in frontier:
				for v in self.adjacency(u):
					if v[0] not in level:
						level[v[0]] = i
						parent[v[0]] = u
						next.append(v[0])
			frontier = next
			i += 1

		return parent

	def topological_sort(self,s):
		parents, visited, time_visited, edge_classifier = self.DFS(s)
		if "Backwards" not in edge_classifier:
			visited.reverse()
			return visited
		else:
			return None

	def dijkstra(self,s):
		deltas = {s:0}
		predecessor = {s: None}
		S = set()
		S.add(s)
		Q = []
		for x in self.vertices:
			if x == s:
				Q.append((0,s))
			else:
				deltas[x] = 999
				predecessor[x] = None

		i = 0
		while len(Q) > 0:
			Q.sort()
			u = Q.pop(0)
			'''
			print("Deltas:", deltas)
			print("U:",u)
			print("S:",S)
			'''
			S.add(u[1])
			for av in self.adjacency(u[1]):
				self.relax(deltas, u[1], av[0], av[1], predecessor)
				if av[0] not in S:
					Q.append((deltas[av[0]],av[0]))
			i += 1
		return predecessor, deltas

	def relax(self, deltas, u, v, w, predecessor):
		if deltas[v] > deltas[u] + w:
			deltas[v] = deltas[u] + w
			predecessor[v] = u


if __name__ == "__main__":

	# Example 1  - Mechanical colours demo from lecture
	#vertices = ['G','Y','P','R','B']
	vertices = ['A', 'H','D','K','G','F','B','J','C','S','Q','Z']

	g = Graph()

	for v in vertices:
		g.add_vertex(v)

	edges = [
		['A','H',11],
		['H', 'D',12 ],
		['D', 'K',52 ],
		['K', 'G',33 ],
		['G', 'F', 41],
		['F', 'B', 19],
		['B', 'J', 3],
		['J', 'C', 14],
		['C', 'S', 4],
		['S', 'Q', 25],
		['Q', 'Z', 16],
		['Z', 'A', 7]
	]
	
	for e in edges:
		g.add_edge(e[0], e[1], e[2])

	print("")
	print("Graph created")
	print("Vertices: ", vertices)
	print("Edges: ", edges)

	'''

	print("")
	print("Carrying out BFS for R from G")
	print("")

	p = g.BFS('G', 'R')

	path = ['B']
	current = path[0]
	while p[current] is not None:
		path.append(p[current])
		current = p[current]

	print("Path: ", path)
	

	vertices = ['A','B','C','D','E','F','G']
	g2 = Graph()
	for v in vertices:
		g2.add_vertex(v)
	edges = [
		['A', 'B', 1],
		['B', 'C', 1],
		#['C', 'A', 1],
		['A', 'G', 1],
		['G', 'C', 1],
		['C', 'D', 1],
		['C', 'F', 1],
		['D', 'E', 1],
		['D', 'F', 1]
	]

	for e in edges:
		g2.add_edge(e[0], e[1], e[2])

	print("")
	print("Vertices: ", vertices)
	print("Edges: ")
	s = '\t'
	for i in range(len(edges)):
		s += str(edges[i]) + ' '
		if i % 4 == 3:
			print(s)
			s = '\t'
	print(s)
	print("")
	print("New Graph created. Carrying out DFS")
	print("")

	p, v, tv, ec = g2.DFS('A')
	print("Parents: ",p)
	print("Visited: ",v)
	print("Time Visited: ",tv)
	print("Edge Classifier: ",ec)

	print("")
	print("Trying topological sort...")
	print("")

	p = g2.topological_sort("A")
	print("Topological Order: ", p)
	
	'''

	print("")
	print("Trying Dijkstra...")
	print("")

	predecessor, deltas = g.dijkstra("A")
	print(predecessor)
	print(deltas)

	print("")
	print("Shortest Paths as follows...")
	print("")

	for v in g.vertices:
		path = [v]
		current = path[0]
		while predecessor[current] is not None:
			path.append(predecessor[current])
			current = predecessor[current]
		path.reverse()
		print("Shortest Path to {} (length {}): {} ".format(v, deltas[v],path))


