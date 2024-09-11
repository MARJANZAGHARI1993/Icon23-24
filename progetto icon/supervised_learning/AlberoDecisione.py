import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Caricamento del file CSV
file_path = 'QUALITA_ARIA_MAGILU2024.csv'  # Inserisci il percorso corretto del file CSV
data = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')

# Pre-elaborazione dei dati
def preprocess_data_for_modeling(df):
    # Sostituzione delle virgole con punti e conversione a numerico
    numeric_cols = ['valore_inquinante_misurato', 'temperatura (°C)', 'Vento (km/h)', 'Umidità (%)']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

    # Codifica delle variabili categoriche
    le = LabelEncoder()
    df['inquinante_misurato_encoded'] = le.fit_transform(df['inquinante_misurato'])
    df['classe_qualita_encoded'] = le.fit_transform(df['classe_qualita'])

    # Definizione di X (feature) e y (target)
    X = df[['valore_inquinante_misurato', 'temperatura (°C)', 'Vento (km/h)', 'Umidità (%)', 'inquinante_misurato_encoded']].dropna()
    y = df.loc[X.index, 'classe_qualita_encoded']

    return X, y, le

# Pre-elaborazione dei dati
X, y, le = preprocess_data_for_modeling(data)

# Trova i nomi delle classi unici originali dall'encoder
class_names = list(le.classes_)
print("Class names:", class_names)

# Visualizzazione del Decision Tree
plt.figure(figsize=(15, 10))
plot_tree(dt_model, feature_names=X.columns, class_names=class_names, filled=True)
plt.title(f'Albero di Decisione con Profondità {best_depth}')
plt.show()


# Normalizzazione delle feature
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Creazione del modello di Decision Tree con profondità scelta
best_depth = 10  # Puoi modificare la profondità in base alle tue esigenze
dt_model = DecisionTreeClassifier(max_depth=best_depth, random_state=42)
dt_model.fit(X_scaled, y)
