import pandas as pd

# Corrected file path
file_path = r'C:\Users\vanpu\OneDrive\Documenten\GitHub\E-Map-Gasunie\Opgeschoonde data\cleaned_data_solar.xlsx'

# Laad de dataset
data = pd.read_excel(file_path)

# Selecteer relevante kolommen
columns_to_keep = ['point', 'type', 'capacity', 'volume', 'percentage', 'validfrom', 'validto']
data = data[columns_to_keep]

# Zet datums om naar datetime-formaat voor eenvoudiger filtering
data['validfrom'] = pd.to_datetime(data['validfrom'])
data['validto'] = pd.to_datetime(data['validto'])

# Voeg een nieuwe kolom toe voor tijdsperiode (optioneel)
data['period'] = data['validfrom'].dt.strftime('%Y-%m-%d %H:%M')

# Mapping van de points naar de juiste latitude en longitude
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
    14: {"latitude": 52.0000, "longitude": 4.0000},  # Offshore (voorbeeld)
    28: {"latitude": 52.1333, "longitude": 3.5125},  # Windpark Luchterduinen
    29: {"latitude": 52.2000, "longitude": 4.0000},  # Windpark Princes Amalia
    30: {"latitude": 52.4700, "longitude": 4.5500},  # Windpark Egmond aan Zee
    31: {"latitude": 53.5500, "longitude": 4.9500},  # Windpark Gemini
    33: {"latitude": 53.5333, "longitude": 3.5833},  # Windpark Borselle I&II
    34: {"latitude": 53.5167, "longitude": 3.6000},  # Windpark Borselle III&IV
    35: {"latitude": 52.3600, "longitude": 4.0600},  # Windpark Hollandse Kust Zuid
    36: {"latitude": 52.4000, "longitude": 4.1200}   # Windpark Hollandse Kust Noord
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
grouped_data.to_excel('prepared_data_solar.xlsx', index=False)

print("De gegevens zijn succesvol voorbereid en opgeslagen in 'prepared_data_with_coordinates.xlsx'.")
