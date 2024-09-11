from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Caricamento del dataset CSV
file_path = 'QUALITA_ARIA_MAGILU2024.csv'  # Inserisci il percorso corretto del tuo file CSV
data = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')

# Pre-elaborazione del dataset: sostituzione delle virgole con punti e conversione a numerico
numeric_cols = ['valore_inquinante_misurato', 'temperatura (°C)', 'Vento (km/h)', 'Umidità (%)']
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col].astype(str).str.replace(',', '.'), errors='coerce')

# Codifica delle variabili categoriali
data['classe_qualita_encoded'] = data['classe_qualita'].astype('category').cat.codes

# Definizione della struttura della Rete Bayesiana
# Struttura dove "Inquinamento" influenza altre variabili
model = BayesianNetwork([('classe_qualita_encoded', 'valore_inquinante_misurato'), 
                         ('classe_qualita_encoded', 'temperatura (°C)'), 
                         ('classe_qualita_encoded', 'Vento (km/h)'),
                         ('classe_qualita_encoded', 'Umidità (%)')])

# Addestramento del modello utilizzando il massimo di verosimiglianza (Maximum Likelihood Estimation)
model.fit(data, estimator=MaximumLikelihoodEstimator)

# Inferenza sulla Rete Bayesiana
inference = VariableElimination(model)

# Esempio di query: probabilità di "classe_qualita_encoded" dato un valore specifico di "temperatura (°C)" e "Umidità (%)"
query_result = inference.query(variables=['classe_qualita_encoded'], 
                               evidence={'temperatura (°C)': 25, 'Umidità (%)': 60})

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
