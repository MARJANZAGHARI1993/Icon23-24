import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn import tree

# Caricamento del dataset (sostituisci con il tuo dataset)
# Ad esempio, usa: dataset = pd.read_csv('tuo_dataset.csv')
# Qui userò un dataset di esempio con variabili temporali e ambientali
data = pd.read_csv('QUALITA_ARIA_MAGILU2024.csv')  # Sostituisci con il nome del tuo dataset

# Visualizza le prime righe del dataset per verificarne il contenuto
print(data.head())

# Preprocessing dei dati: sostituisci eventuali valori NaN con la media della colonna
data = data.fillna(data.mean())

# Definisci le feature (variabili indipendenti) e il target (variabile dipendente)
features = data[['temperatura', 'umidità', 'giorno', 'giorno_settimana', 'livello_inquinante']]  # Sostituisci con le colonne appropriate
target = data['qualità_aria']  # Sostituisci con il nome della colonna target

# Suddivisione del dataset in training e test set (80% training, 20% test)
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Creazione del modello di Albero di Decisione con profondità massima impostata a 11
model = DecisionTreeRegressor(max_depth=11, min_samples_leaf=5, random_state=42)

# Addestramento del modello
model.fit(X_train, y_train)

# Predizione sui dati di test
y_pred = model.predict(X_test)

# Valutazione del modello
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R2): {r2}")

# Visualizzazione dell'Albero di Decisione
plt.figure(figsize=(20,10))
tree.plot_tree(model, feature_names=features.columns, filled=True, fontsize=10)
plt.title('Albero di Decisione per la Qualità dell\'Aria')
plt.show()
