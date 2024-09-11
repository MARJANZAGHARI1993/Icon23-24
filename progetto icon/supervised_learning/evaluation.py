import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt

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

    return X, y

# Pre-elaborazione dei dati
X, y = preprocess_data_for_modeling(data)

# Normalizzazione delle feature
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Inizializzazione di StratifiedKFold per 10 fold
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Modello Albero di Decisione
dt_model = DecisionTreeClassifier(random_state=42)
y_pred_dt = cross_val_predict(dt_model, X_scaled, y, cv=skf)

# Modello Regressione Logistica
lr_model = LogisticRegression(random_state=42, max_iter=1000)
y_pred_lr = cross_val_predict(lr_model, X_scaled, y, cv=skf)

# Clustering con K-Means (non supervisionato)
kmeans_model = KMeans(n_clusters=2, random_state=42)  # Assumiamo 2 cluster
y_pred_kmeans = kmeans_model.fit_predict(X_scaled)

# Funzione per calcolare le metriche di valutazione e creare la tabella
def calculate_metrics(y_true, y_pred, model_name):
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')

    print(f"Metriche per il modello {model_name}:")
    print(f"Accuratezza: {accuracy:.2f}")
    print(f"Precisione: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1:.2f}")
    print("\n")
    
    # Creazione della tabella dei risultati
    metrics = {
        "Model": [model_name],
        "Accuracy": [accuracy],
        "Precision": [precision],
        "Recall": [recall],
        "F1-Score": [f1]
    }
    return pd.DataFrame(metrics)

# Calcolo delle metriche per ciascun modello
metrics_dt = calculate_metrics(y, y_pred_dt, 'Albero di Decisione')
metrics_lr = calculate_metrics(y, y_pred_lr, 'Regressione Logistica')
metrics_kmeans = calculate_metrics(y, y_pred_kmeans, 'K-Means')

# Unione delle tabelle delle metriche
final_metrics_table = pd.concat([metrics_dt, metrics_lr, metrics_kmeans], ignore_index=True)

# Visualizzazione della tabella
print("Tabella delle Metriche:")
print(final_metrics_table.to_string(index=False))

# Salvataggio della tabella in formato CSV
final_metrics_table.to_csv('model_metrics.csv', index=False)

# Funzione per visualizzare la matrice di confusione
def plot_confusion_matrix(y_true, y_pred, model_name):
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap=plt.cm.Blues)
    plt.title(f'Matrice di Confusione - {model_name}')
    plt.show()

# Visualizzazione delle matrici di confusione
plot_confusion_matrix(y, y_pred_dt, 'Albero di Decisione')
plot_confusion_matrix(y, y_pred_lr, 'Regressione Logistica')
plot_confusion_matrix(y, y_pred_kmeans, 'K-Means')