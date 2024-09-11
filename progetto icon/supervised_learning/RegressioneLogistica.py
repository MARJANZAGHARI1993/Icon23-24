import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import LabelBinarizer, LabelEncoder, StandardScaler
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
    data['classe_qualita_encoded'] = le.fit_transform(data['classe_qualita'])

    # Definizione di X (feature) e y (target)
    X = data[['valore_inquinante_misurato', 'temperatura (°C)', 'Vento (km/h)', 'Umidità (%)', 'inquinante_misurato_encoded']].dropna()
    y = data.loc[X.index, 'classe_qualita_encoded']

    # Normalizzazione delle feature
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y

# Percorso al dataset
file_path = 'QUALITA_ARIA_MAGILU2024.csv'  # Inserisci il percorso corretto del file CSV

# Inizializzazione del dataset
X, y = initialize_ML(file_path)

# Inizializzazione di StratifiedKFold per 10 fold
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Modello di Regressione Logistica One-vs-Rest
lr_model = LogisticRegression(random_state=42, max_iter=1000)

# Predizioni probabilistiche utilizzando cross-validation
y_prob_lr = cross_val_predict(lr_model, X, y, cv=skf, method='predict_proba')

# Codifica binaria per la curva ROC multiclass
lb = LabelBinarizer()
y_bin = lb.fit_transform(y)

# Plot della curva ROC per ogni classe
fpr = dict()
tpr = dict()
roc_auc = dict()

for i in range(len(lb.classes_)):
    fpr[i], tpr[i], _ = roc_curve(y_bin[:, i], y_prob_lr[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Plot ROC per ogni classe
plt.figure()
for i in range(len(lb.classes_)):
    plt.plot(fpr[i], tpr[i], lw=2, label=f'Classe {lb.classes_[i]} (area = {roc_auc[i]:.2f})')

plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Curva ROC - Regressione Logistica Multiclasse')
plt.legend(loc="lower right")
plt.grid()
plt.show()
