"""
---MIKJOJGRAPH---

Autori: Grandolfo Michele, Isoardo Jonathan
Data: 10/12/2019
"""

class Graph:

	# Costruttore
	# Riceve
	# 	graphName: nome scelto per il grafo che può essere diverso dal nome dell'oggetto
	def __init__(self, graphName):
		self.graphName = graphName # Variabile per il nome del grafo
		self.graph = {} # Dizionario contenente il grafo
		self.dijkstra = {} # Dizionario contenente i nodi del grafo utilizzato per l'instradamento
		self.path = [] # Lista di utility che memorizza la lista di nodi fornita dall'ultima chiamata di self.findPath_WEIGHT(...)
	
	# toString
	def __str__(self):
		return f"{self.graphName}: {self.graph}\n" # Stringa contenente il nome del grafo e il grafo integrale

	# addNode(): metodo per la creazione di un nodo all'interno del grafo
	# Riceve
	# 	nodeToAdd: nome del nodo da aggiungere al grafo
	def addNode(self, nodeToAdd):
		if nodeToAdd in self.graph: # Controllo per nodo già esistente e conseguente stampa di avviso per errore
			print(f"ERRORE in addNode('{nodeToAdd}')")
			print(f"> Il nodo '{nodeToAdd}' esiste già\n")
		else:
			self.graph[nodeToAdd] = [] # Creazione lista per un nodo all'interno del dizionario del grafo
			self.dijkstra[nodeToAdd] = {} # Creazione di una variabile utilizzata per l'algoritmo di instradamento all'interno del dizionario apposito
			self.dijkstra[nodeToAdd]["weight"] = 0
			self.dijkstra[nodeToAdd]["isVisited"] = False

	# removeNode(): metodo per l'eliminazione di un nodo e tutti gli archi che sono collegati ad esso (sia gli uscenti che gli entranti)
	# Riceve
	# 	nodeToRemove: nome del nodo da rimuovere dal grafo
	def removeNode(self, nodeToRemove):
		if nodeToRemove not in self.graph: # Controllo per nodo non esistente e conseguente stampa di avviso per errore
			print(f"ERRORE in removeNode('{nodeToRemove}')")
			print(f"> Il nodo '{nodeToRemove}' già non esiste\n")
		else:
			self.graph.pop(nodeToRemove) # Eliminazione dell'intera lista di adiacenze del nodo da eliminare e del nodo stesso dal grafo
			self.dijkstra.pop(nodeToRemove) # Eliminazione del nodo dal dizionario di nodi utilizzato per l'instradamento

			for node in self.graph: # Ciclo di scorrimento degli arci di tutti i nodi del grafo
				indexTuple = 0
				for tupl_ in self.graph[node]:
					if nodeToRemove in self.graph[node][indexTuple][0]:
						self.graph[node].pop(indexTuple) # Eliminazione di eventuali archi collegati al nodo da eliminare
					indexTuple += 1

	# addEdge(): metodo per la creazione di un arco all'interno del grafo
	# Riceve
	# 	startNode: nome del nodo di partenza dell'arco
	# 	endNode: nome del nodo di arrivo dell'arco
	# 	weight: peso dell'arco (per grafi non pesati si può inserire 0)
	def addEdge(self, startNode, endNode, weight):
		addEdge = True # Variabile per decidere se l'operazione richiesta è da effettuare
		if startNode not in self.graph or endNode not in self.graph: # Controllo per nodi non esistenti e conseguente stampa di avviso per errore
			addEdge = False # Riassegnazione della variabile per operazione da non effettuare
			print(f"ERRORE in addEdge('{startNode}', '{endNode}', {weight})")
			if startNode not in self.graph:
				print(f"> Il nodo '{startNode}' non esiste")
			if endNode not in self.graph:
				print(f"> Il nodo '{endNode}' non esiste")
			print()
		if self.controlEdge(startNode, endNode) is True: # Controllo per arco esistente tramite funzione apposita e conseguente stampa di avviso per errore
			addEdge = False # Riassegnazione della variabile per operazione da non effettuare
			print(f"ERRORE in addEdge('{startNode}', '{endNode}', {weight})")
			print(f"> L'arco da '{startNode}' a '{endNode}' esite già")

		if addEdge is True: # Controllo per operazione da effettuare
			self.graph[startNode].append((endNode, weight)) # Creazione di un arco, ossia una tupla contenete il nodo di arrio e il peso, all'interno della lista del nodo di partenza

	# addEdge(): metodo per la rimozione di un arco all'interno del grafo
	# Riceve
	# 	startNode: nome del nodo di partenza dell'arco
	# 	endNode: nome del nodo di arrivo dell'arco
	def removeEdge(self, startNode, endNode):
		removeEdge = True # Variabile per decidere se l'operazione richiesta è da effettuare
		if startNode not in self.graph or endNode not in self.graph: # Controllo per nodi non esistenti e conseguente stampa di avviso per errore
			removeEdge = False # Riassegnazione della variabile per operazione da non effettuare
			print(f"ERRORE in addEdge('{startNode}', '{endNode}')")
			if startNode not in self.graph:
				print(f"> Il nodo '{startNode}' non esiste")
			if endNode not in self.graph:
				print(f"> Il nodo '{endNode}' non esiste")
			print()

		if self.controlEdge(startNode, endNode) is False: # Controllo per arco esistente tramite funzione apposita e conseguente stampa di avviso per errore
			removeEdge = False # Riassegnazione della variabile per operazione da non effettuare
			print(f"ERRORE in removeEdge('{startNode}', '{endNode}')")
			print(f"> L'arco da '{startNode}' a '{endNode}' già non esiste")

		if removeEdge is True: # Controllo per operazione da effettuare
			indexTuple = 0
			for tupl_ in self.graph[startNode]: # Ciclo di scorrimento degli archi del nodo di partenza
				if endNode in self.graph[startNode][indexTuple][0]:
					self.graph[startNode].pop(indexTuple) # Rimozione dell'arco da eliminare
				indexTuple += 1

	# controlEdge(): metodo per il controllo dell'esistenza di un arco
	# Riceve
	# 	startNode: nome del nodo di partenza dell'arco
	# 	endNode: nome del nodo di arrivo dell'arco
	# Restituisce
	# 	edgeExist: variabile booleana contenente:
	# 		True -> se l'arco tra i due nodi esiste già
	# 		False -> se l'arco tra i due nodi non esiste ancora
	def controlEdge(self, startNode, endNode):
		edgeExist = False # Variabile per arco esistente o non

		if startNode in self.graph and endNode in self.graph: # Controllo per nodi esistenti
			if self.graph[startNode] != None: # Controllo per archi esistenti nella lista delle adiacenze del nodo
				indexTuple = 0
				for tupl_ in self.graph[startNode]:
					if endNode in self.graph[startNode][indexTuple][0] and edgeExist is False:
						edgeExist = True
					indexTuple += 1

		return edgeExist

	# findPath_WEIGHT(): metodo che avvia l'algoritmo di dijkstra sul grafo per restituire il peso
	# Riceve
	# 	startNode: nome del nodo di partenza dell'algoritmo
	# 	endNode: nome del nodo di arrivo dell'algoritmo
	# Restituisce
	# 	self.dijkstra[endNode]["weight"]: variabile intera contenente:
	# 		-1 -> se il percorso dal nodo di partenza al nodo di arrivo non esiste
	# 		num > 0 -> equivalente al costo minimo per il percorso dal nodo di partenza al nodo di arrivo
	def findPath_WEIGHT(self, startNode, endNode):
		self.inizializateDijskstra(startNode) # Chiamata del metodo per inizializzare il dizionario dijkstra
		
		self.recoursiveDijkstra_WEIGHT(startNode, endNode) # Chiamata del metodo ricorsivo di dijkstra per il calcolo del costo minimo

		return(self.dijkstra[endNode]["weight"])
	
	# findPath_PATH(): metodo che avvia l'algoritmo di dijkstra sul grafo per restituire uno dei percorsi minimi
	# Riceve
	# 	startNode: nome del nodo di partenza dell'algoritmo
	# 	endNode: nome del nodo di arrivo dell'algoritmo
	# Restituisce
	# 	self.path: lista ordinata contenente i nomi dei nodi del percorso minimo
	def findPath_PATH(self, startNode, endNode): 
		self.inizializateDijskstra(startNode) # Chiamata del metodo per inizializzare il dizionario dijkstra
		self.path = [] # Inizializzazione della lista contenente il percorso

		self.recoursiveDijkstra_WEIGHT(startNode, endNode) # Chiamata del metodo ricorsivo di dijkstra per il calcolo del costo minimo
		minCost = self.dijkstra[endNode]["weight"]
		self.recoursiveDijkstra_PATH(startNode, 0, 0, endNode, minCost) # Chiamata del metodo ricorsivo di dijkstra per trovare i nodi del percorso minimo dato il costo

		return self.path


	# recoursiveDijkstra_WEIGHT: metodo ricorsivo che ricompilamento il dizionario di dijkstra in base al dizionario del grafo applicando l'algoritmo di instradamento
	# Riceve
	# 	startNode: nome del nodo di partenza dell'algoritmo
	# 	endNode: nome del nodo di arrivo dell'algoritmo
	def recoursiveDijkstra_WEIGHT(self, startNode, endNode):
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

			self.recoursiveDijkstra_WEIGHT(newStartNode, endNode)

	# recoursiveDijkstra_PATH(): metodo ricorsivo che applica l'algoritmo di dijkstra sul grafo con l'obbiettivo di trovare i nodi presenti nel cammino minimo da un nodo ad un altro
	# Riceve
	# 	startNode: nome del nodo di partenza dell'algoritmo
	# 	actualCost: costo attuale per passare nel percorso in cui ci si trova con la ricorsione (alla prima chiamata bisogna passare 0)
	# 	numNodes: numero di nodi già visitati in un determinato percorso (alla prima chiamata bisogna passare 0 e tra una chiamata )
	# 	endNode: nome del nodo di arrivo dell'algoritmo (non varia tra una chiamata e l'altra)
	# 	minCost: costo minimo per andare dal n
	def recoursiveDijkstra_PATH(self, startNode, actualCost, numNodes, endNode, minCost):
		self.path.append(startNode) # Aggiunta del nodo alla lista del percorso minimo

		if endNode not in self.path: # Condizione per la quale si effettua la ricorsione
			indexTuple = 0
			for tupl_ in self.graph[startNode]: # Ciclo di scorrimento delle adiacenze del nodo di partenza
				if self.graph[startNode][indexTuple][1] + actualCost <= minCost: # Controllo se possibile che il percorso minimo si trovi sull'adiacenza attuale
					newStartNode = self.graph[startNode][indexTuple][0] # Riassegnazione del nodo di partenza
					newActualCost = self.graph[startNode][indexTuple][1] + actualCost # Riasseganzione del costo del percorso parziale
					self.recoursiveDijkstra_PATH(newStartNode, newActualCost, numNodes+1, endNode, minCost)
				indexTuple += 1

			if endNode not in self.path: # Controllo per evitare di rimuovere i nodi corretti una volta che si ha scritto il percorso per intero
				self.path.pop(numNodes) # Rimozione del nodo dalla lista del perscorso minimo in caso il percorso sia errato

			return

	# inizializateDijskstra(): metodo che inizializza il dizionario dijkstra per poter utilizzare l'algoritmo nuovamente
	# Riceve
	# 	startNode: nome del nodo di partenza dell'algoritmo (va inizializzato in modo diverso dagli altri)
	def inizializateDijskstra(self, startNode):
		maxValue = self.maxWeight()

		for node in self .dijkstra: # Ciclo di scorrimento di tutti i nodi del grafo e inizializzazione dei valori nel dizionario dijkstra
			self.dijkstra[node]["weight"] = maxValue
			self.dijkstra[node]["isVisited"] = False

		self.dijkstra[startNode]["weight"] = 0 # Inizializzazione differente per il nodo di partenza

	# maxWeight(): metodo che trova un alternativa a ∞ (infinito) che dovrebbe utilizzare l'algoritmo di dijkstra
	# Ritorna
	# 	graphInfinity: peso massimo moltiplicato per il numero di nodi del grafo
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

	# printGraph_NICE(): stampa in stile più user friendly il grafo rispetto all' __str__
	def printGraph_NICE(self):
		toPrint = f"{self.graphName}: "

		for node in self.graph:
			toPrint += "\n\t" + str(node) + " -> " + str(self.graph[node])

		print(toPrint)
		print()

	# printGraph_NODES(): stampa i nodi del grafo
	def printGraph_NODES(self):
		toPrint = f"{self.graphName} nodes: "

		for node in self.graph:
			toPrint += "'" + str(node) + "' "

		print(toPrint)
		print()

	# printGraph_EDGES(): stampa gli archi del grafo
	def printGraph_EDGES(self):
		toPrint = f"{self.graphName} edges: "

		for node in self.graph:
			indexTuple = 0
			for tupl_ in self.graph[node]:
				toPrint += f"('{node}', '{self.graph[node][indexTuple][0]}', {self.graph[node][indexTuple][1]}) "
				indexTuple += 1

		print(toPrint)
		print()

	# printGraph_DIJKSTRA(): stampa in stile più user friendly il dizionario dijkstra 
	# Utilizzata per fare debugging, solitamente non è utile stampare il dizionario di dijkstra in un programma
	def printGraph_DIJKSTRA(self):
		toPrint = f"{self.graphName} dijkstra: "

		for node in self.dijkstra:
				toPrint += f"\n\t'{node}' -> {self.dijkstra[node]}"

		print(toPrint)
		print()


g = Graph("Grafo bello")
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

print(g)

g.printGraph_NICE()
