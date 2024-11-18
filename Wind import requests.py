import requests
import datetime
import pandas as pd

# API URL en headers
url = "https://api.ned.nl/v1/utilizations"
headers = {
    'X-AUTH-TOKEN': '9c99896102ff51d3bf69eca8796b63e2e0a10b9f9e316645e3b80194d041b4a7',  # Vervang dit met je eigen API-sleutel
    'accept': 'application/ld+json'
}

# Tijdframe voor 2024
start_date = datetime.date(2024, 1, 1)  # Start van 2024
end_date = datetime.date(2024, 12, 31)  # Eind van 2024

# Parameters specifiek voor Wind-2024-Uur-Data
params = {
    'point': 0,  # Nederland
    'type': 1,  # Wind
    'activity': 1,  # Opwekking
    'classification': 2,  # Actuele data
    'granularity': 5,  # Per uur
    'granularitytimezone': 1,  # CET
    'validfrom[after]': str(start_date),
    'validfrom[strictly_before]': str(end_date)
}

# API-verzoek
response = requests.get(url, headers=headers, params=params)

# Controleer de statuscode
if response.status_code == 200:
    data = response.json()
    print(f"Aantal items gevonden: {data.get('hydra:totalItems', 0)}")
    
    # Controleer of er data is
    if 'hydra:member' in data:
        # Data opslaan in een DataFrame
        df = pd.DataFrame(data['hydra:member'])
        
        # Voeg extra kolommen toe
        df['point'] = params['point']
        df['type'] = params['type']
        df['activity'] = params['activity']
        df['classification'] = params['classification']
        df['granularity'] = params['granularity']
        df['timezone'] = params['granularitytimezone']
        
        # Exporteer naar Excel
        df.to_excel("wind_2024_hourly_data.xlsx", index=False)
        print("Data succesvol opgeslagen in wind_2024_hourly_data.xlsx")
    else:
        print("Geen data gevonden voor de opgegeven parameters.")
else:
    print(f"Fout bij ophalen van data: {response.status_code}")
    print(response.text)
