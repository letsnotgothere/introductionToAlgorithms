from Graph import Graph
import csv
import requests
from bs4 import BeautifulSoup

class Country:

	def __init__(self, name, population):
		self.name = name
		self.population = population

def get_bordering_country_pairs():
	BASE_URL = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_number_of_land_borders"
	soup = BeautifulSoup(requests.get(BASE_URL).content, "html.parser")
	i = 0
	pairs = []
	for row in soup.findAll('table')[0].tbody.findAll('tr'):
			if i > 1:
				cell1 = row.find("td").find("a").get_text()
				for c2 in row.findAll("td")[5].findAll("a", title=True):
					c2t = c2.get_text()
					if cell1 is not None and cell1 != "":
						pairs.append((cell1.encode('utf-8'), c2t.encode('utf-8')))
			i += 1
	return pairs


if __name__ == "__main__":

	info_path = r"C:\Users\thoma\Desktop\countries.csv"
	world_map = Graph()
	country_list_text = []
	border_list = get_bordering_country_pairs()

	with open(info_path) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			country_list_text.append(row[0])

	vertices = set(country_list_text)
	edge_u = set(x[0] for x in border_list)
	edge_v = set(x[1] for x in border_list)

	country_dict = {}

	for a in country_list_text:
		country_dict[a] = a

	for x in border_list:
		country_dict[x[0]] = x[0]
		country_dict[x[1]] = x[1]

	countries = country_dict.keys()
	countries.sort()

	for_correction_set = list(set((edge_u - vertices) | (edge_v - vertices) | (vertices - edge_u) | (vertices - edge_v)))
	for_correction_set.sort()

	country_dict["People's Republic of China"] = "China"
	country_dict["C\xc3\xb4te d'Ivoire"] = "Ivory Coast"
	country_dict["Czechia (Czech Republic)"] = "Czech Republic"
	country_dict["Dominica"] = "Dominican Republic"
	country_dict["Eswatini (fmr. \"Swaziland\") "] = "Eswatini"
	country_dict["Holy See"] = "Vatican City"
	country_dict["Palestine State"] = "Palestine"
	country_dict["The Gambia"] = "Gambia"
	country_dict["United States of America"] = "United States"
	country_dict["state of Palestine"] = "Palestine"

	country_list = []

	for c in country_list_text:
		if c in country_dict:
			country_list.append(country_dict[c])
		else:
			print(c)
			print("Error! Not found in dict...")

	corrected_border_list = []

	for x in border_list:
		u = None
		v = None
		if x[0] in country_dict:
			u = country_dict[x[0]]
		else:
			print("Error! U not found in dict...")

		if x[1] in country_dict:
			v = country_dict[x[1]]
		else:
			print("Error! V not found in dict...")

		if u is not None and v is not None:
			corrected_border_list.append((u,v))

	for c in country_list:
		world_map.add_vertex(c)

	for p in corrected_border_list:
		b = False
		if p[0] in country_list and p[1] in country_list:
			world_map.add_edge(p[0],p[1],1)
			b = True
		if b:
			print("Added: ", p)
		else:
			print("Not Added: ", p)



	predecessor, deltas = world_map.dijkstra("North Macedonia")
	print(predecessor)
	print(deltas)

	print("")
	print("Shortest Paths as follows...")
	print("")

	verts = world_map.vertices.keys()
	verts.sort()

	for v in verts:
		path = [v]
		current = path[0]
		while predecessor[current] is not None:
			path.append(predecessor[current])
			current = predecessor[current]
		path.reverse()
		print("Shortest Path to {} (length {}): {} ".format(v, deltas[v], path))


	#print(world_map.edges["Brazil"])
	#print(world_map.adjacency("Brazil"))
