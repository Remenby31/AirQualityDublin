import numpy as np
from scipy.interpolate import RegularGridInterpolator, griddata
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import os

def afficherMatrice3D(matrice3D):
    # affichage de la matrice 3D
    for i in range(0, matrice3D.shape[0]):
        plt.clf()
        plt.imshow(matrice3D[i])
        plt.plot()

def sauvegarderPNG(matrice3D, nomDossier: str):
    # sauvegarde de la matrice 3D

    #creation du dossier
    if not os.path.exists(nomDossier):
        os.makedirs(nomDossier)

    for i in range(0, matrice3D.shape[0]):
        #on sauvegarde les n premières matrices sous la forme d'une image
        plt.imsave(nomDossier + "/matrice" + str(i) + ".png", matrice3D[i])

def sauvegardePNGAll(Lmatrice3D, Lmatrice3D_Name, nomDossier : str):
    # Lmatrice3D : liste des matrices 3D à sauvegarder
    # Lmatrice3D_Name : liste des noms des matrices 3D à sauvegarder
    # Lposition : liste des positions des matrices 3D à sauvegarder dans le subplot

    #creation du dossier
    if not os.path.exists(nomDossier):
        os.makedirs(nomDossier)

    # On plot les matrices sur différentes figures en carré et on sauvegarde
    for i in range(0, Lmatrice3D[0].shape[0]):
        plt.clf()
        for j in range(0, len(Lmatrice3D)):
            plt.subplot(2, len(Lmatrice3D)//2, j+1)
            plt.imshow(Lmatrice3D[j][i])
            plt.title(Lmatrice3D_Name[j])
        plt.savefig(nomDossier + "/matrice" + str(i) + ".png")

def interpolationSpline(data):
    # Créez un masque pour les valeurs manquantes
    missing_values_mask = data == 0

    # Obtenez les indices des valeurs manquantes et des valeurs existantes
    missing_indices = np.argwhere(missing_values_mask)
    existing_indices = np.argwhere(~missing_values_mask)

    # Obtenez les valeurs existantes à partir des indices
    existing_values = data[~missing_values_mask]

    # Utilisez griddata pour interpoler les valeurs manquantes en utilisant l'interpolation spline (linear)
    print("Interpolation des valeurs manquantes en cours...")
    estimated_values = griddata(existing_indices, existing_values, missing_indices, method='linear', fill_value=0)
    print("Interpolation des valeurs manquantes terminée.")

    # Remplacez les valeurs manquantes dans la matrice de données par les valeurs interpolées
    data[missing_values_mask] = estimated_values
    
    return data

def knn_impute_3d(data, n_neighbors=5, alpha=0.9):
    # n_neighbors : nombre de voisins à considérer
    # alpha : poids de l'espace par rapport au temps
    #       alpha = 1 : on considère uniquement l'espace
    #       alpha = 0 : on considère uniquement le temps

    data_copy = data.copy()

    missing_values_mask = data_copy == 0
    missing_indices = np.argwhere(missing_values_mask)
    existing_indices = np.argwhere(~missing_values_mask)
    existing_values = data_copy[~missing_values_mask]

    # Créez un modèle NearestNeighbors pour trouver les voisins les plus proches
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto').fit(existing_indices)
    
    # Trouvez les indices des k plus proches voisins pour chaque valeur manquante
    distances, indices = nbrs.kneighbors(missing_indices)
    
    # Créez un tableau pour stocker les valeurs estimées
    estimated_values = np.zeros(missing_indices.shape[0])

    # Calculez la moyenne pondérée des k plus proches voisins pour chaque valeur manquante
    for i in range(missing_indices.shape[0]):
        # Si le voisin est le même jour, on lui donne un poids de alpha
        # Sinon, on lui donne un poids de 1 - alpha
        weights = np.array([alpha if missing_indices[i][0] == existing_indices[indices[i][j]][0] else 1 - alpha for j in range(n_neighbors)])
        weights /= weights.sum()
        estimated_values[i] = np.dot(weights, existing_values[indices[i]])

    # Remplacez les valeurs manquantes dans la matrice de données par les valeurs estimées
    data_copy[missing_values_mask] = estimated_values

    return data_copy
    


# ==================== Chargement des données ====================

matrix3D_pm25 = np.load('matrix3D_pm25_v2.npy')

# ==================== Traitement des valeurs manquantes ====================

print("calcul de knn/S")
matrix3D_pm25_knn_S = knn_impute_3d(matrix3D_pm25, n_neighbors=10, alpha=0.9)
print("Sauvegarde des knn/S")
sauvegarderPNG(matrix3D_pm25_knn_S, 'matrix3D_pm25_KNN_S')

print("calcul de knn/M")
matrix3D_pm25_knn_M = knn_impute_3d(matrix3D_pm25, n_neighbors=10, alpha=0.5)
print("Sauvegarde des knn/M")
sauvegarderPNG(matrix3D_pm25_knn_M, 'matrix3D_pm25_KNN_M')

print("calcul de knn/T")
matrix3D_pm25_knn_T = knn_impute_3d(matrix3D_pm25, n_neighbors=10, alpha=0.1)
print("Sauvegarde des knn/T")
sauvegarderPNG(matrix3D_pm25_knn_T, 'matrix3D_pm25_KNN_T')

sauvegardePNGAll([matrix3D_pm25, matrix3D_pm25_knn_S, matrix3D_pm25_knn_M, matrix3D_pm25_knn_T],["Base", "KNN-S", "KNN-M", "KNN-T"], "matrix3D_pm25_KNN")


