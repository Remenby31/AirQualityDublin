import numpy as np
from scipy.interpolate import CubicSpline
from scipy.interpolate import griddata
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt


def impute_knn(data, n_neighbors=5, alpha=0.9):
    print("-> KNN with alpha = ", alpha)
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

def fast_impute_knn(data, n_neighbors=5, alpha=0.9):
    print("-> KNN with alpha =", alpha)

    data_copy = data.copy()
    missing_values_mask = data_copy == 0
    missing_indices = np.argwhere(missing_values_mask)
    existing_indices = np.argwhere(~missing_values_mask)
    existing_values = data_copy[~missing_values_mask]

    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto').fit(existing_indices)
    distances, indices = nbrs.kneighbors(missing_indices)

    estimated_values = np.zeros(missing_indices.shape[0])

    for i in range(missing_indices.shape[0]):
        weights = np.array([alpha if missing_indices[i][0] == existing_indices[indices[i][j]][0] else 1 - alpha for j in range(n_neighbors)])
        weights /= weights.sum()
        estimated_values[i] = np.dot(weights, existing_values[indices[i]])

    data_copy[missing_values_mask] = estimated_values

    return data_copy

def impute_interpolationT(matrix3D):
    print("-> interpolation temporelle")
    # Remplace les zeros par des Nan
    matrix3D_nan = matrix3D.copy()
    matrix3D_nan[matrix3D_nan == 0] = np.nan
    for i in range (matrix3D_nan.shape[1]):
        for j in range (matrix3D_nan.shape[2]):
            Lx = np.arange(matrix3D_nan.shape[0])[~np.isnan(matrix3D_nan[:,i,j])]
            Lx = Lx.astype(float)
            Ly = matrix3D_nan[:,i,j][~np.isnan(matrix3D_nan[:,i,j])]
            if Lx.size ==0:
                pass
            elif Lx.size < 20:
                matrix3D_nan[:,i,j] = np.mean(Ly)
            else:
                # Condition aux limites (dérivée nulle à gauche et à droite)
                Lx = np.concatenate(([-2, -1], Lx, [matrix3D_nan.shape[0], matrix3D_nan.shape[0] + 1]))
                Ly = np.concatenate(([Ly[0], Ly[0]], Ly, [Ly[-1], Ly[-1]]))
                # Interpolation
                spline = CubicSpline(Lx, Ly, bc_type='not-a-knot')
                # On récupère les indices des valeurs manquantes
                missing_values_mask = np.isnan(matrix3D_nan[:,i,j])
                # On recalcule les valeurs interpolées et on les clippe pour qu'elles soient comprises entre 0 et max(Ly)
                new_Ly = spline(np.arange(matrix3D_nan.shape[0])[missing_values_mask])
                new_Ly_truncated = np.clip(new_Ly, min(Ly), max(Ly))
                # On remplace les valeurs manquantes par les valeurs interpolées
                matrix3D_nan[missing_values_mask,i,j] = new_Ly_truncated
    np.nan_to_num(matrix3D_nan, copy=False)
    return matrix3D_nan

def impute_interpolationS(matrix3D, method='nearest'):
    print("-> interpolation Spatialle")
    # Remplace les zeros par des Nan
    matrix3D_nan = matrix3D.copy()
    matrix3D_nan[matrix3D_nan == 0] = np.nan

    for i in range(matrix3D_nan.shape[0]):
        if np.isnan(matrix3D_nan[i,:,:]).sum() < matrix3D_nan.shape[1] * matrix3D_nan.shape[2]:
            matrix2D = matrix3D_nan[i,:,:]
            # Obtenez les indices des valeurs manquantes
            missing_values_mask = np.isnan(matrix2D)

            # On stocker les valeurs min et max de la matrice pour les utiliser pour clipper les valeurs interpolées
            min_value = np.nanmin(matrix2D)
            max_value = np.nanmax(matrix2D)

            # Créez des matrices de coordonnées pour les axes x et y
            X, Y = np.meshgrid(np.arange(matrix2D.shape[0]), np.arange(matrix2D.shape[1]), indexing='ij')

            # Utilisez uniquement les valeurs non manquantes pour créer le modèle d'interpolation
            X_known = X[~missing_values_mask]
            Y_known = Y[~missing_values_mask]
            Z_known = matrix2D[~missing_values_mask]

            # Créez un ensemble de points à partir des coordonnées connues
            known_points = np.column_stack((X_known.ravel(), Y_known.ravel()))

            # Interpolez les valeurs manquantes en utilisant griddata
            X_missing = X[missing_values_mask]
            Y_missing = Y[missing_values_mask]
            missing_points = np.column_stack((X_missing.ravel(), Y_missing.ravel()))
            matrix2D[missing_values_mask] = griddata(known_points, Z_known, missing_points, method=method)
            
            # clippe les valeurs pour qu'elles soient comprises entre min(matrix2D) et max(matrix2D)
            matrix2D = np.nan_to_num(matrix2D)
            matrix2D = np.clip(matrix2D, min_value, max_value)

            # Remplacez les valeurs manquantes dans la matrice de données par les valeurs interpolées
            matrix3D_nan[i,:,:] = matrix2D

    np.nan_to_num(matrix3D_nan, copy=False)
    return matrix3D_nan

def impute_interpolationST(matrix3D):
    matrix3D_new = matrix3D.copy()
    matrix3D_new = impute_interpolationT(matrix3D_new)
    matrix3D_new = impute_interpolationS(matrix3D_new)
    return matrix3D_new