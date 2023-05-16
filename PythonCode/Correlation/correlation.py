import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
matrix = np.load("matrix3D_pm25_v2.npy")

# load the csv file Dublin 2021-10-01 to 2022-07-31.csv

df = pd.read_csv("Dublin 2021-10-01 to 2022-07-31.csv", delimiter=";")

def determine_correlation(matrix, X):
    moyenne_temperature_jour = np.mean(matrix, axis=(1, 2))
    X = np.delete(X, -1)
    coefficient_correlation = np.corrcoef(moyenne_temperature_jour, X)[0, 1]

    return coefficient_correlation

def Sauvegarder_colonnes_csv(df, noms_colonnes):
    df = df[noms_colonnes]
    df.to_csv("weatherDataCorrel.csv", index=False, sep=";")

L = []

for i in range(df.shape[1]):
    try:
        score = determine_correlation(matrix, np.array(df[df.columns[i]].values))
        if not(math.isnan(score)):
            L.append([score, df.columns[i]])
    except:
        pass

noms_colonnes = [x[1] for x in L]
Sauvegarder_colonnes_csv(df, noms_colonnes)

# Affichage des scores de corrélation sous forme d'un graphique à barres
L.sort(reverse=True)

scores, labels = zip(*L)
y_pos = np.arange(len(labels))

plt.bar(y_pos, scores, align='center', alpha=0.5)
plt.xticks(y_pos, labels, rotation='vertical')
plt.ylabel("Correlation scores")
plt.title("Correlation between weather and pollution data (pm2.5)")

plt.tight_layout()
plt.show()