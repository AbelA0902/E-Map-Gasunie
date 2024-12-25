import requests
import datetime
import pandas as pd

# API-configuratie
url = "https://api.ned.nl/v1/utilizations"
headers = {
    'X-AUTH-TOKEN': '9c99896102ff51d3bf69eca8796b63e2e0a10b9f9e316645e3b80194d041b4a7',
    'accept': 'application/ld+json'
}

# Datuminstellingen
start_date = "2023-01-01"  # Begin van de data
today = datetime.date.today()  # Huidige datum

# Parameters die eenvoudig aanpasbaar zijn
points = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
types = [2]  # Wind
activities = [1]  # Providing
classifications = [1, 2, 3]  # Current
granularities = [5]  # Per uur
granularity_timezones = [1]  # CET

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

# Lijst voor het opslaan van alle data
all_data = []

# Itereren over alle parametercombinaties
for point in points:
    for energy_type in types:
        for activity in activities:
            for classification in classifications:
                for granularity in granularities:
                    for timezone in granularity_timezones:
                        # Paginering: Startpagina is 1
                        page = 1
                        while True:
                            params = {
                                'point': point,
                                'type': energy_type,
                                'activity': activity,
                                'granularity': granularity,
                                'granularitytimezone': timezone,
                                'classification': classification,
                                'validfrom[after]': start_date,
                                'validfrom[strictly_before]': str(today),
                                'page': page  # Specifieer de pagina
                            }

                            # API-verzoek
                            response = requests.get(url, headers=headers, params=params)
                            print(f"Status code: {response.status_code} - Page: {page}")  # Statuscode check
                            if response.status_code == 200:
                                data = response.json()
                                if data.get('hydra:totalItems', 0) > 0:
                                    for item in data['hydra:member']:
                                        # Voeg locatiegegevens toe
                                        item['latitude'] = location_mapping[point]['latitude']
                                        item['longitude'] = location_mapping[point]['longitude']
                                        item['point'] = point
                                        item['type'] = energy_type
                                        item['activity'] = activity
                                        item['classification'] = classification
                                        item['granularity'] = granularity
                                        item['timezone'] = timezone

                                        all_data.append(item)

                                    # Als er meer items zijn, gaan we door naar de volgende pagina
                                    if 'hydra:view' in data and 'hydra:next' in data['hydra:view']:
                                        page += 1
                                    else:
                                        break  # Geen volgende pagina, we stoppen
                                else:
                                    break  # Geen data gevonden voor deze combinatie, we stoppen
                            else:
                                print(f"Fout bij ophalen van data. Punt: {point}, Status code: {response.status_code}")
                                print(response.text)
                                break

# Controleer hoeveel data is verzameld
print(f"Aantal rijen verzameld: {len(all_data)}")

# Data opslaan in Excel
if all_data:
    df = pd.DataFrame(all_data)
    file_name = "Fossil_Data_with_Location.xlsx"
    df.to_excel(file_name, index=False)
    print(f"Data succesvol opgeslagen in {file_name}")
else:
    print("Geen data om op te slaan.")
