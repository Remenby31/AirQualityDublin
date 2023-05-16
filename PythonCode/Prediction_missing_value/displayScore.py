import numpy as np
from diplaySave import *
from imputeMethods import impute_interpolationST, fast_impute_knn
from score_MissingValue import score, delete_random_points
import neuronne
import matrix

mat = matrix.matrix()
neuronne = neuronne.MachineLearning(weather=True)

# ==================== Chargement des données ====================

matrix3D_pm25 = np.load('matrix3D_pm25_v2.npy')

# ==================== Traitement des valeurs manquantes ====================

matrix3D_emputed = delete_random_points(matrix3D_pm25, 500, 7)

matrix3D_KNN = fast_impute_knn(matrix3D_emputed, 10, alpha = 0.5)
matrix3D_KNN_S = fast_impute_knn(matrix3D_emputed, 10, alpha = 0.1)
matrix3D_KNN_T = fast_impute_knn(matrix3D_emputed, 10, alpha = 0.9)

matrix3D_interpolationST = impute_interpolationST(matrix3D_emputed)

neuronne.train_randomForest(matrix3D_emputed)
matrix3D_randomForest = neuronne.predict_randomForest(matrix3D_emputed)

neuronne.train_regressionLineaire(matrix3D_emputed)
matrix3D_regressionLineaire = neuronne.predict_regressionLineaire(matrix3D_emputed)

neuronne.train_regressionLasso(matrix3D_emputed)
matrix3D_regressionLasso = neuronne.predict_regressionLasso(matrix3D_emputed)

neuronne.train_regressionRidge(matrix3D_emputed)
matrix3D_regressionRidge = neuronne.predict_regressionRidge(matrix3D_emputed)

neuronne.train_GBM(matrix3D_emputed)
matrix3D_GBM = neuronne.predict_GBM(matrix3D_emputed)

neuronne.train_ANN(matrix3D_emputed)
matrix3D_ANN = neuronne.predict_ANN(matrix3D_emputed)

# ==================== Score des matrices ====================

MSE, MAE, R2 = score(matrix3D_pm25, matrix3D_KNN)
print("MSE KNN : ", MSE, " MAE KNN : ", MAE, " R2 KNN : ", R2)

MSE, MAE, R2 = score(matrix3D_pm25, matrix3D_KNN_S)
print("MSE KNN_S : ", MSE, " MAE KNN_S : ", MAE, " R2 KNN_S : ", R2)

MSE, MAE, R2 = score(matrix3D_pm25, matrix3D_KNN_T)
print("MSE KNN_T : ", MSE, " MAE KNN_T : ", MAE, " R2 KNN_T : ", R2)

MSE, MAE, R2 = score(matrix3D_pm25, matrix3D_interpolationST)
print("MSE interpolationST : ", MSE, " MAE interpolationST : ", MAE, " R2 interpolationST : ", R2)

MSE, MAE, R2 = score(matrix3D_pm25, matrix3D_randomForest)
print("MSE randomForest : ", MSE, " MAE randomForest : ", MAE, " R2 randomForest : ", R2)

MSE, MAE, R2 = score(matrix3D_pm25, matrix3D_regressionLineaire)
print("MSE regressionLineaire : ", MSE, " MAE regressionLineaire : ", MAE, " R2 regressionLineaire : ", R2)

MSE, MAE, R2 = score(matrix3D_pm25, matrix3D_regressionLasso)
print("MSE regressionLasso : ", MSE, " MAE regressionLasso : ", MAE, " R2 regressionLasso : ", R2)

MSE, MAE, R2 = score(matrix3D_pm25, matrix3D_regressionRidge)
print("MSE regressionRidge : ", MSE, " MAE regressionRidge : ", MAE, " R2 regressionRidge : ", R2)

MSE, MAE, R2 = score(matrix3D_pm25, matrix3D_GBM)
print("MSE GBM : ", MSE, " MAE GBM : ", MAE, " R2 GBM : ", R2)

MSE, MAE, R2 = score(matrix3D_pm25, matrix3D_ANN)
print("MSE ANN : ", MSE, " MAE ANN : ", MAE, " R2 ANN : ", R2)