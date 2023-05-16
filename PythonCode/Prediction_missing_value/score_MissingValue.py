import numpy as np

def delete_points_arround(matrix_3d, point, radius):
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            for k in range(-radius, radius + 1):
                if point[0] + i >= 0 and point[0] + i < matrix_3d.shape[0] and point[1] + j >= 0 and point[1] + j < matrix_3d.shape[1] and point[2] + k >= 0 and point[2] + k < matrix_3d.shape[2]:
                    matrix_3d[point[0] + i, point[1] + j, point[2] + k] = 0
    return matrix_3d

def delete_random_points(matrix_3d, Nbpoints, radius=3):
    # On supprime Nbpoints parties de la matrice aléatoirement 
    matrix_3d = matrix_3d.copy()
    Nb_points_deleted = 0
    while Nb_points_deleted < Nbpoints:
        point = (np.random.randint(0, matrix_3d.shape[0]),
                 np.random.randint(0, matrix_3d.shape[1]),
                 np.random.randint(0, matrix_3d.shape[2]))
        if matrix_3d[point] != 0:
            matrix_3d = delete_points_arround(matrix_3d, point, radius)
            Nb_points_deleted += 1
    return matrix_3d

def score(matrice_base, matrice_predict):
    # On calcule le score MSE (Mean Squared Error) entre la matrice 3D et la matrice 3D estimée
    MSE = 0
    Nb_points = 0
    for i in range(0, matrice_base.shape[0]):
        for j in range(0, matrice_base.shape[1]):
            for k in range(0, matrice_base.shape[2]):
                if matrice_base[i, j, k] != 0:
                    MSE += (matrice_base[i, j, k] - matrice_predict[i, j, k])**2
                    Nb_points += 1
    MSE = MSE / Nb_points

    # On calcule le score MAE (Mean Absolute Error) entre la matrice 3D et la matrice 3D estimée
    MAE = 0
    for i in range(0, matrice_base.shape[0]):
        for j in range(0, matrice_base.shape[1]):
            for k in range(0, matrice_base.shape[2]):
                if matrice_base[i, j, k] != 0:
                    MAE += abs(matrice_base[i, j, k] - matrice_predict[i, j, k])
    MAE = MAE / Nb_points

    # On calcule le Coefficient de détermination R² entre la matrice 3D et la matrice 3D estimée

    # On calcule la moyenne de la matrice 3D
    moyenne = 0
    for i in range(0, matrice_base.shape[0]):
        for j in range(0, matrice_base.shape[1]):
            for k in range(0, matrice_base.shape[2]):
                if matrice_base[i, j, k] != 0:
                    moyenne += matrice_base[i, j, k]
    moyenne = moyenne / Nb_points

    # On calcule la somme des carrés des écarts à la moyenne
    somme_ecarts_carres = 0
    for i in range(0, matrice_base.shape[0]):
        for j in range(0, matrice_base.shape[1]):
            for k in range(0, matrice_base.shape[2]):
                if matrice_base[i, j, k] != 0:
                    somme_ecarts_carres += (matrice_base[i, j, k] - moyenne)**2

    # On calcule la somme des carrés des écarts entre la matrice 3D et la matrice 3D estimée
    somme_ecarts_estimes_carres = 0
    for i in range(0, matrice_base.shape[0]):
        for j in range(0, matrice_base.shape[1]):
            for k in range(0, matrice_base.shape[2]):
                if matrice_base[i, j, k] != 0:
                    somme_ecarts_estimes_carres += (matrice_base[i, j, k] - matrice_predict[i, j, k])**2
        
    R2 = 1 - (somme_ecarts_estimes_carres / somme_ecarts_carres)

    return MSE, MAE, R2

