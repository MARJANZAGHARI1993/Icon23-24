import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Caricamento del dataset (sostituisci con il tuo dataset)
data = pd.read_csv('QUALITA_ARIA_MAGILU2024.csv')  # Sostituisci con il nome del tuo dataset

# Visualizza le prime righe del dataset per verificarne il contenuto
print(data.head())

# Definisci la variabile target (ad esempio, se il livello di PM2.5 supera una soglia critica)
data['target'] = (data['PM2.5'] > 50).astype(int)  # Cambia 'PM2.5' e la soglia a seconda del tuo dataset

# Selezione delle feature per il modello (variabili ambientali e temporali)
features = data[['temperatura', 'umidità', 'livello_inquinante', 'giorno']]  # Sostituisci con le tue colonne

# Preprocessing dei dati: gestione dei valori mancanti
features = features.fillna(features.mean())

# Suddivisione del dataset in training e test set
X_train, X_test, y_train, y_test = train_test_split(features, data['target'], test_size=0.2, random_state=42)

# Standardizzazione delle feature
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Inizializzazione e addestramento del modello di Regressione Logistica
model = LogisticRegression(C=1.0, solver='liblinear', random_state=42)
model.fit(X_train_scaled, y_train)

# Previsione sul test set
y_pred = model.predict(X_test_scaled)

# Valutazione delle prestazioni del modello
print("Matrice di Confusione:")
print(confusion_matrix(y_test, y_pred))
print("\nReport di Classificazione:")
print(classification_report(y_test, y_pred))
print("\nAccuratezza del modello:")
print(accuracy_score(y_test, y_pred))

# Visualizzazione della matrice di confusione
plt.figure(figsize=(6, 4))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predetto')
plt.ylabel('Reale')
plt.title('Matrice di Confusione per Regressione Logistica')
plt.show()
