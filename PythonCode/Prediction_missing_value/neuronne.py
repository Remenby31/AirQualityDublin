import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.neural_network import MLPRegressor
from matrix import matrix
import pandas as pd

class MachineLearning:
    def __init__(self, weather=True):
        self.model = None
        self.weather = weather
    
    # ==== Preparation des données ====
    
    def preparer_entrainement(self, matrix_3d):
        matrix = matrix_3d.copy()
        matrix[matrix == 0] = np.nan
        # On récupère les coordonées de toutes les valeurs différente de np.nan de la matrice 3D
        indices = np.where(~np.isnan(matrix))

        # On récupère les données d'entrainement
        X = np.array([indices[0], indices[1], indices[2]]).T

        # On récupère les données méteo dans le fichier weatherDataCorrel.csv
        # et on ajoute les données météo, dont la ligne correspond à l'indice 0 de la matrice 3D
        if self.weather:
            weatherData = pd.read_csv("weatherDataCorrel.csv", sep=";")
            X = np.concatenate((X, weatherData.values[indices[0]]), axis=1)

        # Normaliser les données
        X[:,0] = X[:,0] / matrix.shape[0]
        X[:,1] = X[:,1] / matrix.shape[1]
        X[:,2] = X[:,2] / matrix.shape[2]

        y = matrix[indices]

        return X, y
    
    def preparer_prediction(self, matrix_3d):
        # On récupère les coordonées de toutes les valeurs np.nan de la matrice 3D
        matrix_3d[matrix_3d == 0] = np.nan
        indices = np.where(np.isnan(matrix_3d))

        # On récupère les données à prédire
        X = np.array([indices[0], indices[1], indices[2]]).T

        # On récupère les données méteo dans le fichier weatherDataCorrel.csv
        # et on ajoute les données météo, dont la ligne correspond à l'indice 0 de la matrice 3D
        if self.weather:
            weatherData = pd.read_csv("weatherDataCorrel.csv", sep=";")
            X = np.concatenate((X, weatherData.values[indices[0]]), axis=1)

        # Normaliser les données
        X[:,0] = X[:,0] / matrix_3d.shape[0]
        X[:,1] = X[:,1] / matrix_3d.shape[1]
        X[:,2] = X[:,2] / matrix_3d.shape[2]

        return X, indices
    
    # ==== Modèles de Machine Learning ====
                    
    def train_randomForest(self, matrix_3d):

        X, y = self.preparer_entrainement(matrix_3d)

        # On entraine le modèle
        print("[ML - RandomForest] Training model...")
        model = RandomForestRegressor()
        model.fit(X, y)
        print("[ML - RandomForest] Model trained")
        self.model = model

    def predict_randomForest(self, matrix_3d):
        matrix = matrix_3d.copy()
        
        X, indices = self.preparer_prediction(matrix)

        # Prediction
        print("[ML - RandomForest] Predicting...")
        y_pred = self.model.predict(X)

        # On ajoute les prédictions au matrix_3d
        print("[ML - RandomForest] Adding predictions to matrix...")
        matrix[indices] = y_pred

        return matrix

    def train_regressionLineaire(self, matrix_3d):
        X, y = self.preparer_entrainement(matrix_3d)

        # On entraine le modèle
        print("[ML - LinearRegression] Training model...")
        model = LinearRegression()
        model.fit(X, y)
        print("[ML - LinearRegression] Model trained")
        self.model = model

    def predict_regressionLineaire(self, matrix_3d):
        matrix = matrix_3d.copy()

        X, indices = self.preparer_prediction(matrix)

        # Prediction
        print("[ML - LinearRegression] Predicting...")
        y_pred = self.model.predict(X)

        # On ajoute les prédictions au matrix_3d
        print("[ML - LinearRegression] Adding predictions to matrix...")
        matrix[indices] = y_pred

        return matrix
    
    def train_regressionLasso(self, matrix_3d):
        X, y = self.preparer_entrainement(matrix_3d)

        # On entraine le modèle
        print("[ML - Lasso] Training model...")
        model = Lasso()
        model.fit(X, y)
        print("[ML - Lasso] Model trained")
        self.model = model
    
    def predict_regressionLasso(self, matrix_3d):
        matrix = matrix_3d.copy()
        X, indices = self.preparer_prediction(matrix)

        # Prediction
        print("[ML - Lasso] Predicting...")
        y_pred = self.model.predict(X)

        # On ajoute les prédictions au matrix_3d
        print("[ML - Lasso] Adding predictions to matrix...")
        matrix[indices] = y_pred

        return matrix
    
    def train_regressionRidge(self, matrix_3d):
        X, y = self.preparer_entrainement(matrix_3d)

        # On entraine le modèle
        print("[ML - Ridge] Training model...")
        model = Ridge()
        model.fit(X, y)
        print("[ML - Ridge] Model trained")
        self.model = model

    def predict_regressionRidge(self, matrix_3d):
        matrix = matrix_3d.copy()
        X, indices = self.preparer_prediction(matrix)

        # Prediction
        print("[ML - Ridge] Predicting...")
        y_pred = self.model.predict(X)

        # On ajoute les prédictions au matrix_3d
        print("[ML - Ridge] Adding predictions to matrix...")
        matrix[indices] = y_pred

        return matrix
    
    def train_GBM(self, matrix_3d):
        X, y = self.preparer_entrainement(matrix_3d)

        # On entraine le modèle
        print("[ML - GBM] Training model...")
        model = GradientBoostingRegressor()
        model.fit(X, y)
        print("[ML - GBM] Model trained")
        self.model = model

    def predict_GBM(self, matrix_3d):
        matrix = matrix_3d.copy()
        X, indices = self.preparer_prediction(matrix_3d)

        # Prediction
        print("[ML - GBM] Predicting...")
        y_pred = self.model.predict(X)

        # On ajoute les prédictions au matrix_3d
        print("[ML - GBM] Adding predictions to matrix...")
        matrix[indices] = y_pred

        return matrix
    
    def train_ANN(self, matrix_3d):
        X, y = self.preparer_entrainement(matrix_3d)

        # On entraine le modèle
        print("[ML - ANN] Training model...")
        model = MLPRegressor()
        model.fit(X, y)
        print("[ML - ANN] Model trained")
        self.model = model
    
    def predict_ANN(self, matrix_3d):
        matrix = matrix_3d.copy()
        X, indices = self.preparer_prediction(matrix)

        # Prediction
        print("[ML - ANN] Predicting...")
        y_pred = self.model.predict(X)

        # On ajoute les prédictions au matrix_3d
        print("[ML - ANN] Adding predictions to matrix...")
        matrix[indices] = y_pred

        return matrix
    