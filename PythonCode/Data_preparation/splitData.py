import os
from pandas import read_csv
import datetime

def timestamp_minuit(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(midnight.timestamp())

# On revient en arriere dans le dossier
os.chdir('..')

# List all the files in the directory
files = os.listdir('DCU/')
# Create a list of the files that end with .csv
csvFiles = [file for file in files if file.endswith('.csv')]


# Loop through the list of files
for file in csvFiles:
    # Read the file into a DataFrame
    df = read_csv("DCU/" + file, delimiter=';')

    try:
        # Recperer le premier timestamp
        firstTimestamp = df['timestamp'].iloc[0]
        timestampMin = timestamp_minuit(firstTimestamp)
    except:
        print("Error with file " + file)
        continue

    # === Fixed data ===
    if file.split('_')[1] == 'fixed':
        print("[Fixed] Traitement du fichier " + file)
        # On recupere les coordonnées des stations dans le fichier fixed_station_locations.csv
        fixedStationLocations = read_csv("DCU/fixed_station_location.csv", delimiter=';')

        print("[Fixed] Ajout des coordonnées des stations")

        # pour chaque ligne de file, on ajoute les coordonnées de la station apres timestamp
        for index, row in df.iterrows():
            stationId = row['sensor ID']
            stationRow = fixedStationLocations[fixedStationLocations['sensor ID'] == stationId]
            df.at[index, 'latitude'] = stationRow['latitude'].iloc[0]
            df.at[index, 'longitude'] = stationRow['longitude'].iloc[0]

        print("[Fixed] Ecriture des fichiers csv")
        
        # Pour chaque jour, on creer un fichier csv avec les donnees du jour et les headers (les données sont triées par timestamp)
        while True:
            try:
                # On recupere les timestamp du jour
                timestampMax = timestampMin + 86400

                # On recupere les lignes du jour
                dayDf = df[(df['timestamp'] >= timestampMin) & (df['timestamp'] < timestampMax)]
                if len(dayDf) == 0:
                    break

                # on creer un dossier pour le fichier, si il n'existe pas
                if not os.path.exists("DCU/" + file[:-4]):
                    os.makedirs("DCU/" + file[:-4])

                # On creer le nom du fichier avec le timestamp du jour, converti en date
                fileName = "DCU/" + file[:-4] + '/' + datetime.datetime.fromtimestamp(timestampMin).strftime('%Y-%m-%d') + '.csv'

                # On ecrit le fichier, sans ajouter les headers
                dayDf.to_csv(fileName, index=False, header=False, sep=';')

                # On passe au jour suivant
                timestampMin = timestampMax
            except:
                print("Error with file " + file)

    # === Mobile data ===
    elif file.split('_')[1] == 'mobiles':
        print("[Mobile] Traitement du fichier " + file)
        # Pour chaque jour, on creer un fichier csv avec les donnees du jour et les headers (les données sont triées par timestamp)

        while True:
            try:
                # On recupere les timestamp du jour
                timestampMax = timestampMin + 86400

                # On recupere les lignes du jour
                dayDf = df[(df['timestamp'] >= timestampMin) & (df['timestamp'] < timestampMax)]
                if len(dayDf) == 0:
                    break

                # on creer un dossier pour le fichier, si il n'existe pas
                if not os.path.exists("DCU/" + file[:-4]):
                    os.makedirs("DCU/" + file[:-4])

                # On creer le nom du fichier avec le timestamp du jour, converti en date
                fileName = "DCU/" + file[:-4] + '/' + datetime.datetime.fromtimestamp(timestampMin).strftime('%Y-%m-%d') + '.csv'

                # On ecrit le fichier, sans ajouter les headers
                dayDf.to_csv(fileName, index=False, header=False, sep=';')

                # On passe au jour suivant
                timestampMin = timestampMax
            except:
                print("Error with file " + file)