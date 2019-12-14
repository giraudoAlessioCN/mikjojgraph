class Graph:

	def __init__(self):
		self.graph = {} # Dizionario contenente il grafo
		self.dijkstra = {} # Dizionario contenente i nodi del grafo utilizzato per l'instradamento

	def __str__(self):
		return f"{self.graph}" # Stringa contenente il nome del grafo e il grafo integrale

	def addNode(self, nodeToAdd):
		if nodeToAdd not in self.graph: # Controllo per nodo già esistente e conseguente stampa di avviso per errore
			self.graph[nodeToAdd] = [] # Creazione lista per un nodo all'interno del dizionario del grafo
			self.dijkstra[nodeToAdd] = {} # Creazione di una variabile utilizzata per l'algoritmo di instradamento all'interno del dizionario apposito
			self.dijkstra[nodeToAdd]["weight"] = 0
			self.dijkstra[nodeToAdd]["isVisited"] = False

	def addEdge(self, startNode, endNode, weight):
		if startNode in self.graph and endNode in self.graph: # Controllo per nodi non esistenti e conseguente stampa di avviso per errore
			self.graph[startNode].append((endNode, weight)) # Creazione di un arco, ossia una tupla contenete il nodo di arrio e il peso, all'interno della lista del nodo di partenza

	def findPath(self, startNode, endNode):
		self.inizializateDijskstra(startNode) # Chiamata del metodo per inizializzare il dizionario dijkstra
		self.recoursiveDijkstra(startNode, endNode) # Chiamata del metodo ricorsivo di dijkstra per il calcolo del costo minimo
		return(self.dijkstra[endNode]["weight"])

	def recoursiveDijkstra(self, startNode, endNode):
		if startNode is None: # Controllo per percorso non esistente
			self.dijkstra[endNode]["weight"] = -1
		
		if startNode is not None and startNode is not endNode: # Condizione per la quale si effetua la ricorsione
			self.dijkstra[startNode]["isVisited"] = True # Marcatura del nodo di partenza come visitato
			
			indexTuple = 0
			for tupl_ in self.graph[startNode]: # Ciclo di scorrimento delle adiacenze del nodo di partenza e conseguente compilamento del dizionario dijktra secondo l'algoritmo
				adiacent = self.graph[startNode][indexTuple][0] # Variabile di utilità per la lettura di un adiacenza
				edgeWeight = self.graph[startNode][indexTuple][1] # Variabile di utilità per la lettura del peso dell'adiacenza
				if startNode != adiacent and self.dijkstra[adiacent]["weight"] > (self.dijkstra[startNode]["weight"] + edgeWeight): # Controllo per il ricompilamento del dizionario dijkstra
					self.dijkstra[adiacent]["weight"] = self.dijkstra[startNode]["weight"] + edgeWeight # Compilazione del nodo adiacente
				indexTuple += 1

			minWeight = self.maxWeight() # Impostazione di un peso massimo (irraggiungibile) calcolato in base al garfo
			newStartNode = None # Impostazione nel prossimo nodo come None per casi di percorso non esistente
			for node in self.dijkstra:
				if self.dijkstra[node]["isVisited"] is False and self.dijkstra[node]["weight"] < minWeight:
						minWeight = self.dijkstra[node]["weight"] # Riassegnazione del peso minimo
						newStartNode = node # Riassegnazione del nodo di partenza

			self.recoursiveDijkstra(newStartNode, endNode)

	def inizializateDijskstra(self, startNode):
		maxValue = self.maxWeight()
		for node in self .dijkstra: # Ciclo di scorrimento di tutti i nodi del grafo e inizializzazione dei valori nel dizionario dijkstra
			self.dijkstra[node]["weight"] = maxValue
			self.dijkstra[node]["isVisited"] = False

		self.dijkstra[startNode]["weight"] = 0 # Inizializzazione differente per il nodo di partenza

	
	def maxWeight(self):
		numberOfNode = 0 # Variabile che conta il numero di nodi del grafo
		maxWeight = 0 # Variabile per il peso massimo
		for node in self.graph: # Ciclo di scorrimento degli arci di tutti i nodi del grafo
			indexTuple = 0

			for tupl_ in self.graph[node]:
				if self.graph[node][indexTuple][1] > maxWeight:
					maxWeight = self.graph[node][indexTuple][1] # Riassegnazione del massimo peso trovato
				indexTuple += 1

			numberOfNode += 1
		graphInfinity = maxWeight * numberOfNode # Moltiplicazione tra il peso massim trovato e il numero di nodi
		return graphInfinity

print()

g = Graph()

g.addNode("A")
g.addNode("B")
g.addNode("C")
g.addNode("D")
g.addNode("E")
g.addEdge("A", "B", 1)
g.addEdge("A", "C", 2)
g.addEdge("A", "D", 3)
g.addEdge("B", "E", 9)
g.addEdge("C", "E", 6)
g.addEdge("D", "E", 2)

print("g ->", g)
print()

start = "A"
end = "E"
cost = g.findPath(start, end)
print(f"Il costo per andare da {start} a {end} è di {cost}")
print()