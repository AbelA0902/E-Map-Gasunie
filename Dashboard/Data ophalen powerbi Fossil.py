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
points = [0, 14]
types = [18]  # Wind
activities = [1]  # Providing
classifications = [1, 2, 3]  # Current
granularities = [5]  # Per uur
granularity_timezones = [1]  # CET

# Mapping van de points naar de juiste provincie
location_mapping = {
    0: "Nederland",
    1: "Groningen",
    2: "Friesland",
    3: "Drenthe",
    4: "Overijssel",
    5: "Flevoland",
    6: "Gelderland",
    7: "Utrecht",
    8: "Noord-Holland",
    9: "Zuid-Holland",
    10: "Zeeland",
    11: "Noord-Brabant",
    12: "Limburg",
    14: "Offshore",
    28: "Windpark Luchterduinen",
    29: "Windpark Princes Amalia",
    30: "Windpark Egmond aan Zee",
    31: "Windpark Gemini",
    33: "Windpark Borselle I&II",
    34: "Windpark Borselle III&IV",
    35: "Windpark Hollandse Kust Zuid",
    36: "Windpark Hollandse Kust Noord"
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
                                        # Voeg provinciegegevens toe
                                        item['province'] = location_mapping[point]
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
    file_name = "Fossil_Data_with_Provinces.xlsx"
    df.to_excel(file_name, index=False)
    print(f"Data succesvol opgeslagen in {file_name}")
else:
    print("Geen data om op te slaan.")
