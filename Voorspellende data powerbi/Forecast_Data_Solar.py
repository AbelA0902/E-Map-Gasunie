import requests
import pandas as pd
import datetime

# API-configuratie
API_URL = "https://api.ned.nl/v1/utilizations"
headers = {
    'X-AUTH-TOKEN': '9c99896102ff51d3bf69eca8796b63e2e0a10b9f9e316645e3b80194d041b4a7',
    'accept': 'application/ld+json'
}

# Datuminstellingen
start_date = "2025-01-01"  # Begin van de data
end_date = "2025-12-31"  # Eind van de data

# Parameters die eenvoudig aanpasbaar zijn
points = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
types = [2]  # Zon
activities = [1]  # Providing
classifications = [1]  # Forecast
granularities = [6]  # Per dag
granularity_timezones = [1]  # CET

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
                                'validfrom[strictly_before]': end_date,
                                'page': page  # Specifieer de pagina
                            }

                            # API-verzoek
                            response = requests.get(API_URL, headers=headers, params=params)
                            print(f"Status code: {response.status_code} - Page: {page}")  # Statuscode check
                            if response.status_code == 200:
                                data = response.json()
                                if data.get('hydra:totalItems', 0) > 0:
                                    for item in data['hydra:member']:
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

# Zet de verzamelde data om in een pandas DataFrame
df = pd.DataFrame(all_data)

# Sla de DataFrame op als Excel-bestand
df.to_excel('forecast_data_solar_2025.xlsx', index=False)

print("Data succesvol opgehaald en opgeslagen in forecast_data_solar_2025.xlsx")
