import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Funzione per caricare e pre-elaborare il dataset
def initialize_ML(file_path):
    # Caricamento del file CSV
    data = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')

    # Sostituzione delle virgole con punti e conversione a numerico
    numeric_cols = ['valore_inquinante_misurato', 'temperatura (°C)', 'Vento (km/h)', 'Umidità (%)']
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col].astype(str).str.replace(',', '.'), errors='coerce')

    # Codifica delle variabili categoriche
    le = LabelEncoder()
    data['inquinante_misurato_encoded'] = le.fit_transform(data['inquinante_misurato'])

    # Definizione di X (feature)
    X = data[['valore_inquinante_misurato', 'temperatura (°C)', 'Vento (km/h)', 'Umidità (%)', 'inquinante_misurato_encoded']].dropna()

    # Normalizzazione delle feature
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled

# Percorso al dataset
file_path = 'QUALITA_ARIA_MAGILU2024.csv'  # Inserisci il percorso corretto del file CSV

# Inizializzazione del dataset
X = initialize_ML(file_path)
# Applicazione dell'algoritmo K-Means con diversi valori di k
sse = []  # Somma degli errori quadrati all'interno dei cluster
range_k = range(1, 11)  # Testiamo k da 1 a 10

for k in range_k:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    sse.append(kmeans.inertia_)  # Inertia rappresenta la somma delle distanze al quadrato dai punti al loro centroide più vicino

# Visualizzazione del metodo del gomito
plt.figure()
plt.plot(range_k, sse, marker='o', linestyle='-', color='b')
plt.title('Metodo del Gomito per Determinare il Numero Ottimale di Cluster')
plt.xlabel('Numero di Cluster (k)')
plt.ylabel('Somma degli Errori Quadrati (Inertia)')
plt.grid()
plt.show()
