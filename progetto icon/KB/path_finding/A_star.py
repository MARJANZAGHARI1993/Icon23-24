import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue

def heuristic(a, b):
    """Funzione euristica per A* (distanza euclidea)"""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def a_star_algorithm(graph, start, goal):
    """Algoritmo A* per trovare il percorso più breve"""
    # Coda di priorità per i nodi da esplorare
    open_set = PriorityQueue()
    open_set.put((0, start))
    
    # Dizionario per memorizzare il percorso
    came_from = {start: None}
    
    # Distanza attuale dal nodo iniziale
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0
    
    # Stima del costo totale dal nodo iniziale al nodo finale passando per il nodo corrente
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = heuristic(graph.nodes[start]['pos'], graph.nodes[goal]['pos'])
    
    while not open_set.empty():
        current = open_set.get()[1]
        
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + heuristic(graph.nodes[current]['pos'], graph.nodes[neighbor]['pos'])
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(graph.nodes[neighbor]['pos'], graph.nodes[goal]['pos'])
                open_set.put((f_score[neighbor], neighbor))
    
    return None  # Nessun percorso trovato

# Creazione del grafo
G = nx.Graph()

# Definizione dei nodi con le loro posizioni (x, y)
nodes = {
    'A': (0, 0), 
    'B': (1, 2), 
    'C': (2, 1), 
    'D': (3, 0), 
    'E': (4, 2), 
    'F': (5, 1)
}

# Aggiunta dei nodi al grafo con le posizioni
for node, pos in nodes.items():
    G.add_node(node, pos=pos)

# Aggiunta degli archi (con pesi rappresentanti la distanza tra i nodi)
edges = [
    ('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('B', 'E'), ('D', 'F'), ('E', 'F')
]

G.add_edges_from(edges)

# Esecuzione dell'algoritmo A*
start_node = 'A'
goal_node = 'F'
path = a_star_algorithm(G, start_node, goal_node)

# Visualizzazione del grafo e del percorso trovato
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=16)
if path:
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    print(f"Percorso trovato da {start_node} a {goal_node}: {path}")
else:
    print("Nessun percorso trovato")

plt.show()
