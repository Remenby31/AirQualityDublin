from neuronne import MachineLearning
import numpy as np
import matrix

mat = matrix.matrix()
ML = MachineLearning()

matrix3D_pm25 = np.load('matrix3D_pm25_v2.npy')

ML.train_randomForest(matrix3D_pm25)

matrix3D_pm25_randomForest = ML.predict_randomForest(matrix3D_pm25)

mat.filter_uniform(matrix3D_pm25_randomForest, 20)

mat.export_csv_fast(matrix3D_pm25_randomForest, matrix3D_pm25_randomForest, "matrix3D_pm25_randomForest")
