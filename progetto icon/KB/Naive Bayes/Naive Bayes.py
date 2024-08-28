from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Creazione di un dataset di esempio
data = pd.DataFrame(data={'Temperatura': ['Alta', 'Alta', 'Bassa', 'Bassa', 'Alta'],
                          'Umidità': ['Alta', 'Alta', 'Alta', 'Bassa', 'Bassa'],
                          'Inquinamento': ['Elevato', 'Elevato', 'Moderato', 'Basso', 'Moderato'],
                          'Vento': ['Debole', 'Forte', 'Forte', 'Debole', 'Forte']})

# Definizione della struttura della Rete Bayesiana
model = BayesianNetwork([('Temperatura', 'Inquinamento'), 
                         ('Umidità', 'Inquinamento'), 
                         ('Vento', 'Inquinamento')])

# Addestramento del modello utilizzando il massimo di verosimiglianza (Maximum Likelihood Estimation)
model.fit(data, estimator=MaximumLikelihoodEstimator)

# Inferenza sulla Rete Bayesiana
inference = VariableElimination(model)

# Esempio di query: probabilità dell'inquinamento dato che la temperatura è 'Alta' e l'umidità è 'Bassa'
query_result = inference.query(variables=['Inquinamento'], 
                               evidence={'Temperatura': 'Alta', 'Umidità': 'Bassa'})

print(query_result)

# Creazione di un grafo NetworkX manualmente
graph = nx.DiGraph()

# Aggiungi nodi e archi dalla rete bayesiana
for edge in model.edges():
    graph.add_edge(edge[0], edge[1])

# Visualizzazione della struttura della rete
pos = nx.spring_layout(graph)  # Layout per la visualizzazione
nx.draw(graph, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=16, edge_color='gray')
plt.title("Struttura della Rete Bayesiana")
plt.show()
