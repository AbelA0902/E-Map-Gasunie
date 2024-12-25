import pandas as pd
# Corrected file path
data_file_path = r'C:\Users\vanpu\OneDrive\Documenten\GitHub\E-Map-Gasunie\Opgeschoonde data\cleaned_data_windoffshore.xlsx'

# Laad de dataset
data = pd.read_excel(data_file_path)

# Selecteer relevante kolommen
columns_to_keep = ['point', 'type', 'capacity', 'volume', 'percentage', 'validfrom', 'validto']
data = data[columns_to_keep]

# Zet datums om naar datetime-formaat voor eenvoudiger filtering
data['validfrom'] = pd.to_datetime(data['validfrom'])
data['validto'] = pd.to_datetime(data['validto'])

# Voeg een nieuwe kolom toe voor tijdsperiode (optioneel)
data['period'] = data['validfrom'].dt.strftime('%Y-%m-%d %H:%M')

# Mapping van de points naar de juiste latitude en longitude (update volgens handleiding)
location_mapping = {
    0: {"latitude": 52.3784, "longitude": 4.9009},  # Nederland
    1: {"latitude": 53.2194, "longitude": 6.5665},  # Groningen
    2: {"latitude": 53.2012, "longitude": 5.7998},  # Friesland
    3: {"latitude": 52.9035, "longitude": 6.6177},  # Drenthe
    4: {"latitude": 52.4975, "longitude": 6.0765},  # Overijssel
    5: {"latitude": 52.4095, "longitude": 5.4864},  # Flevoland
    6: {"latitude": 52.2298, "longitude": 5.2830},  # Gelderland
    7: {"latitude": 52.0907, "longitude": 5.1214},  # Utrecht
    8: {"latitude": 52.3794, "longitude": 4.9009},  # Noord-Holland
    9: {"latitude": 52.0106, "longitude": 4.4945},  # Zuid-Holland
    10: {"latitude": 51.4584, "longitude": 3.6580},  # Zeeland
    11: {"latitude": 51.5857, "longitude": 5.1207},  # Noord-Brabant
    12: {"latitude": 50.8814, "longitude": 5.8691},  # Limburg
    # Extra locaties of nieuwe punten volgens de handleiding hier toevoegen
}

# Voeg de latitude en longitude toe aan de dataset
def get_coordinates(point):
    return location_mapping.get(point, {"latitude": None, "longitude": None})

# Apply the get_coordinates function to each row
coordinates = data['point'].apply(lambda x: get_coordinates(x))

# Expand the dictionary into separate latitude and longitude columns
data[['latitude', 'longitude']] = pd.DataFrame(coordinates.tolist(), index=data.index)

# Groepeer de data per punt of type voor aggregaties
grouped_data = data.groupby(['point', 'type']).agg({
    'capacity': 'sum',
    'volume': 'sum',
    'percentage': 'mean',
    'latitude': 'first',  # Gebruik de eerste waarde van latitude en longitude
    'longitude': 'first'  # Gebruik de eerste waarde van latitude en longitude
}).reset_index()

# Opslaan naar een nieuw Excel-bestand voor visualisatie in Power BI
output_file_path = r'C:\Users\vanpu\OneDrive\Documenten\GitHub\E-Map-Gasunie\prepared_data_fossilgaspowercorrect.xlsx'
grouped_data.to_excel(output_file_path, index=False)

print(f"De gegevens zijn succesvol voorbereid en opgeslagen in '{output_file_path}'.")
