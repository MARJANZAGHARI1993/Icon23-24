import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Caricamento del dataset (sostituisci con il tuo dataset)
# Ad esempio, usa: dataset = pd.read_csv('tuo_dataset.csv')
# Qui userò un dataset di esempio con variabili temporali e ambientali
data = pd.read_csv('QUALITA_ARIA_MAGILU2024.csv')  # Sostituisci con il nome del tuo dataset

# Visualizza le prime righe del dataset per verificarne il contenuto
print(data.head())

# Preprocessing dei dati: sostituisci eventuali valori NaN con la media della colonna
data = data.fillna(data.mean())

# Definisci le feature da usare per il clustering (ad esempio, variabili ambientali)
features = data[['temperatura', 'umidità', 'livello_inquinante']]  # Sostituisci con le colonne appropriate

# Standardizzazione delle feature per il clustering (K-means è sensibile alle diverse scale dei dati)
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Applicazione dell'algoritmo K-means con 3 cluster
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
kmeans.fit(features_scaled)

# Assegna ogni punto al cluster più vicino
clusters = kmeans.predict(features_scaled)
data['Cluster'] = clusters

# Visualizzazione dei risultati del clustering
plt.figure(figsize=(8, 6))
plt.scatter(data['temperatura'], data['umidità'], c=data['Cluster'], cmap='viridis', marker='o', edgecolor='k')
plt.xlabel('Temperatura')
plt.ylabel('Umidità')
plt.title('Clustering K-means sulla Qualità dell\'Aria')
plt.show()

# Visualizzazione delle coordinate dei centroidi
print("Coordinate dei Centroidi dei Cluster:")
print(kmeans.cluster_centers_)
