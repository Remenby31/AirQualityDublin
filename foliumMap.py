import folium
import pandas as pd
from ipywidgets import interact


file_path = "DCU/test.csv"


# Chargez vos données à partir du fichier csv
data = pd.read_csv(file_path, sep=';')

# Convertir la colonne timestamp en datetime pour pouvoir la filtrer
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Créez une carte en utilisant folium
map = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Définir une fonction pour filtrer les données en fonction de la date
def update_map(selected_date):
    filtered_data = data[data['timestamp'].dt.date == selected_date.date()]
    for lat, lon, pm25, pm10 in zip(filtered_data['latitude'], filtered_data['longitude'], filtered_data['pm2.5(ug/m3)'], filtered_data['pm10(ug/m3)']):
        folium.CircleMarker([lat, lon], radius=pm25/20, color='red', fill=True).add_to(map)

# Créer un widget de filtrage de date
interact(update_map, selected_date=data['timestamp'].sort_values().unique());

# Sauvegarder la carte dans un fichier html
map