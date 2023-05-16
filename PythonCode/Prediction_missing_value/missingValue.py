import numpy as np
from diplaySave import *
from imputeMethods import impute_knn, impute_interpolationT, impute_interpolationS
from score_MissingValue import score, delete_random_points
import neuronne
import matrix

mat = matrix.matrix()
neuronne = neuronne.MachineLearning()

# ==================== Chargement des données ====================

matrix3D_pm25 = np.load('matrix3D_pm25_v2.npy')

# ==================== Ecriture des données dans le fichier csv ====================


# ==================== Traitement des valeurs manquantes ====================

matrix3D_pm25 = impute_interpolationS(matrix3D_pm25, method='nearest')

neuronne.train_randomForest(matrix3D_pm25)
matrix3D_randomForest = neuronne.predict_randomForest(matrix3D_pm25)

neuronne.train_regressionLineaire(matrix3D_pm25)
matrix3D_regressionLineaire = neuronne.predict_regressionLineaire(matrix3D_pm25)

neuronne.train_regressionLasso(matrix3D_pm25)
matrix3D_regressionLasso = neuronne.predict_regressionLasso(matrix3D_pm25)

neuronne.train_regressionRidge(matrix3D_pm25)
matrix3D_regressionRidge = neuronne.predict_regressionRidge(matrix3D_pm25)

neuronne.train_GBM(matrix3D_pm25)
matrix3D_GBM = neuronne.predict_GBM(matrix3D_pm25)

neuronne.train_ANN(matrix3D_pm25)
matrix3D_ANN = neuronne.predict_ANN(matrix3D_pm25)

# ==================== Copie des données ====================

matrix3D_randomForest_brut = matrix3D_randomForest.copy()
matrix3D_regressionLineaire_brut = matrix3D_regressionLineaire.copy()
matrix3D_regressionLasso_brut = matrix3D_regressionLasso.copy()
matrix3D_regressionRidge_brut = matrix3D_regressionRidge.copy()
matrix3D_GBM_brut = matrix3D_GBM.copy()
matrix3D_ANN_brut = matrix3D_ANN.copy()

# ==================== Filtrage des données ====================

mat.filter_uniform(matrix3D_randomForest, 20)
mat.filter_uniform(matrix3D_regressionLineaire, 20)
mat.filter_uniform(matrix3D_regressionLasso, 20)
mat.filter_uniform(matrix3D_regressionRidge, 20)
mat.filter_uniform(matrix3D_GBM, 20)
mat.filter_uniform(matrix3D_ANN, 20)

# ==================== Sauvegarde des matrices ====================

np.save('matrix3D_randomForest.npy', matrix3D_randomForest_brut)
np.save('matrix3D_regressionLineaire.npy', matrix3D_regressionLineaire_brut)
np.save('matrix3D_regressionLasso.npy', matrix3D_regressionLasso_brut)
np.save('matrix3D_regressionRidge.npy', matrix3D_regressionRidge_brut)
np.save('matrix3D_GBM.npy', matrix3D_GBM_brut)
np.save('matrix3D_ANN.npy', matrix3D_ANN_brut)

# ==================== Exportation des matrices ====================

mat.export_csv_fast(matrix3D_randomForest, matrix3D_randomForest, "matrix3D_randomForest_filtre")
mat.export_csv_fast(matrix3D_regressionLineaire, matrix3D_regressionLineaire, "matrix3D_regressionLineaire_filtre")
mat.export_csv_fast(matrix3D_regressionLasso, matrix3D_regressionLasso, "matrix3D_regressionLasso_filtre")
mat.export_csv_fast(matrix3D_regressionRidge, matrix3D_regressionRidge, "matrix3D_regressionRidge_filtre")
mat.export_csv_fast(matrix3D_GBM, matrix3D_GBM, "matrix3D_GBM_filtre")
mat.export_csv_fast(matrix3D_ANN, matrix3D_ANN, "matrix3D_ANN_filtre")