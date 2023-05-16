import os
import shutil
import pandas as pd
import numpy as np
from scipy.ndimage import uniform_filter


class matrix:
    def __init__(self, size_matrix=300, date_min="2021-10-01", date_max="2022-07-31", longitude_hautGauche=-6.385765160158097, latitude_hautGauche=53.40770831718198, longitude_basDroit=-6.157192225564314, latitude_basDroit=53.27289327467902):

        # === Coordonate & date ===
        self.longitude_hautGauche = longitude_hautGauche
        self.latitude_hautGauche = latitude_hautGauche
        self.longitude_basDroit = longitude_basDroit
        self.latitude_basDroit = latitude_basDroit

        self.date_min = date_min
        self.date_max = date_max

        # === Matrix ===
        nbJour= (pd.to_datetime(date_max, format='%Y-%m-%d') - pd.to_datetime(date_min, format='%Y-%m-%d')).days
        self.size_matrix = size_matrix
        self.matrix_pm25 = np.zeros((nbJour, size_matrix, size_matrix))
        self.matrix_pm10 = np.zeros((nbJour, size_matrix, size_matrix))

    def getDayMatrix(self, file_path):

        # On creer la matrice du jour
        dayMatrix_pm25 = np.zeros((self.size_matrix, self.size_matrix))
        dayMatrix_pm10 = np.zeros((self.size_matrix, self.size_matrix))

        # Si le fichier n'existe pas, on renvoit la matrice du jour vide
        if file_path == FileNotFoundError:
            return dayMatrix_pm25, dayMatrix_pm10

        # On recupere le contenu du fichier du jour
        dayDf = pd.read_csv(file_path, header=None, sep=';', dtype=float)

        # On recupere la taille d'un point dans la matrice
        dlongitude = abs((self.longitude_hautGauche - self.longitude_basDroit) / self.size_matrix)
        dlatitude = abs((self.latitude_hautGauche - self.latitude_basDroit) / self.size_matrix)

        # Pour chaque point dans la matrice
        for i in range(self.size_matrix):
            
            latitude_min = self.latitude_basDroit + i * dlatitude - 5 * dlatitude
            latitude_max = self.latitude_basDroit + (i+1) * dlatitude + 5 * dlatitude

            for j in range( self.size_matrix):

                # On recupere les coordonnes du point
                longitude_min = self.longitude_hautGauche + j * dlongitude - 5 * dlongitude
                longitude_max = self.longitude_hautGauche + (j+1) * dlongitude + 5 * dlongitude

                # On recupere les points dans le fichier du jour
                dayDfPointLongitude = dayDf[(dayDf[5] >= longitude_min) & (dayDf[5] <= longitude_max)]
                dayDfPoint = dayDfPointLongitude[(dayDfPointLongitude[4] >= latitude_min) & (dayDfPointLongitude[4] <= latitude_max)]

                # Si il y a des points dans le fichier du jour, on fait la moyenne et on l'ajoute a la matrice du jour
                if dayDfPoint.shape[0] > 0:
                    dayMatrix_pm25[i,j] = dayDfPoint[3].mean()
                    dayMatrix_pm10[i,j] = dayDfPoint[4].mean()
                # Sinon on met 0
                else:
                    dayMatrix_pm25[i,j] = 0
                    dayMatrix_pm10[i,j] = 0
            
        return dayMatrix_pm25, dayMatrix_pm10
        
    def get_liste_date(self, date_min, date_max):
        # On renvoit une liste avec toutes les dates entre date_min et date_max
        liste_date = []
        date = pd.to_datetime(date_min, format='%Y-%m-%d')
        date_max = pd.to_datetime(date_max, format='%Y-%m-%d')
        while date <= date_max:
            liste_date.append(date.strftime("%Y-%m-%d") + ".csv")
            date += pd.Timedelta(days=1)
        return liste_date
    
    def find_file(self, file_name):
        # On liste les dossiers
        liste_dossier = os.listdir(".")
        # Pour tous les dossiers mixtes, on cherche le fichier
        for dossier in liste_dossier:
            if len(dossier.split("_")) > 1 and dossier.split("_")[1] == "mixed":
                liste_fichier = os.listdir(dossier)
                if file_name in liste_fichier:
                    return dossier + "/" + file_name
        return FileNotFoundError
        
    
    def getMatrix(self):
        # On recupere la liste des nom de fichier
        files = self.get_liste_date(self.date_min, self.date_max)

        # Pour chaque fichier
        for i in range(np.shape(self.matrix_pm25)[0]):
            # On convertit i en une date, (nombre de jour depuis date_min)
            date = pd.to_datetime(self.date_min, format='%Y-%m-%d') + pd.Timedelta(days=i)
            dayMatrix_pm25, dayMatrix_pm10 = self.getDayMatrix(self.find_file(date.strftime("%Y-%m-%d") + ".csv"))

            # On ajoute la matrice du jour a la matrice globale
            self.matrix_pm25[i] = dayMatrix_pm25
            self.matrix_pm10[i] = dayMatrix_pm10

            print("Matrice du jour " + str(i) + " / " + str(np.shape(self.matrix_pm25)[0]) + " : " + date.strftime("%Y-%m-%d") + " OK !" )

        return self.matrix_pm25, self.matrix_pm10
    
    def export_csv(self, matrix_pm25, matrix_pm10, name):
        # on créer le dossier avec le nom name, si il existe deja, on le supprime
        if os.path.exists(name):
            shutil.rmtree(name)
        os.mkdir(name)

        # On export la matrice en csv sous le même format que le fichier d'origine
        for i in range(np.shape(matrix_pm25)[0]):
            date = pd.to_datetime(self.date_min, format='%Y-%m-%d') + pd.Timedelta(days=i)
            # pour chaque point de la matrice, on écrit dans le fichier csv
            # format [timestamp, id, pm25, pm10, latitude, longitude]
            with open(name + "/" + date.strftime("%Y-%m-%d") + ".csv", 'w') as f:
                for j in range(np.shape(matrix_pm25)[1]):
                    for k in range(np.shape(matrix_pm25)[2]):
                        timestamp = int((pd.to_datetime(self.date_min, format='%Y-%m-%d') + pd.Timedelta(days=i) + pd.Timedelta(hours=12)).timestamp())
                        id = 0
                        longitude = self.longitude_hautGauche + k * abs((self.longitude_hautGauche - self.longitude_basDroit) / self.size_matrix)
                        latitude = self.latitude_basDroit + j * abs((self.latitude_hautGauche - self.latitude_basDroit) / self.size_matrix)
                        pm25 = matrix_pm25[i,j,k]
                        pm10 = matrix_pm10[i,j,k]
                        f.write(str(timestamp) + ";" + str(id) + ";" + str(pm25) + ";" + str(pm10) + ";" + str(latitude) + ";" + str(longitude) + "\n")
            print("Export du jour " + str(i) + " / " + str(np.shape(matrix_pm25)[0]) + " : " + date.strftime("%Y-%m-%d") + " OK !" )

    def export_csv_fast(self, matrix_pm25, matrix_pm10, name):
        # On crée le dossier avec le nom name, si il existe déjà, on le supprime
        if os.path.exists(name):
            shutil.rmtree(name)
        os.mkdir(name)

        matrix_shape = np.shape(matrix_pm25)
        
        # On calcule les pas de longitude et latitude
        longitude_step = abs((self.longitude_hautGauche - self.longitude_basDroit) / self.size_matrix)
        latitude_step = abs((self.latitude_hautGauche - self.latitude_basDroit) / self.size_matrix)

        # On exporte la matrice en csv sous le même format que le fichier d'origine
        for i in range(matrix_shape[0]):
            date = pd.to_datetime(self.date_min, format='%Y-%m-%d') + pd.Timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            timestamp = int((date + pd.Timedelta(hours=12)).timestamp())
            
            # Pour chaque point de la matrice, on écrit dans le fichier csv
            # Format [timestamp, id, pm25, pm10, latitude, longitude]
            with open(os.path.join(name, date_str + ".csv"), 'w') as f:
                for j in range(matrix_shape[1]):
                    latitude = self.latitude_basDroit + j * latitude_step
                    for k in range(matrix_shape[2]):
                        longitude = self.longitude_hautGauche + k * longitude_step
                        pm25 = matrix_pm25[i, j, k]
                        pm10 = matrix_pm10[i, j, k]
                        f.write(f"{timestamp};0;{pm25};{pm10};{latitude};{longitude}\n")

            print(f"Export du jour {i} / {matrix_shape[0]} : {date_str} OK !")
    
    def filter_uniform(self, matrix, size_filter):
        print("Filtrage uniforme de la matrice")
        for day in range(np.shape(matrix)[0]):
            # on applique un filtre box sur la matrice de taille size_filter
            matrix[day] = uniform_filter(matrix[day], size=size_filter, mode='constant')
        print("Filtrage uniforme de la matrice OK !")

                        
                                