import requests
import datetime
import pandas as pd

# Basisinformatie voor de API-aanroep
url = "https://api.ned.nl/v1/utilizations"
headers = {'X-AUTH-TOKEN': '9c99896102ff51d3bf69eca8796b63e2e0a10b9f9e316645e3b80194d041b4a7',
           'accept': 'application/ld+json'}

today = datetime.date.today()
last_week = today - datetime.timedelta(days=1000)  # Periode instellen

# Parameters voor de API
points = [0,14]  # Voor heel Nederland en offshore
types = [17]  # Wind offshore
activities = [1]  # Providing
classifications = [1,2,3]  # Forecast, current, backcast
granularities = [6]  # Groepering per tijdsinterval
granularity_timezones = [0, 1]  # Tijdzones

all_data = []

# Itereren over de combinaties van parameters
for point in points:
    for energy_type in types:
        for activity in activities:
            for classification in classifications:
                for granularity in granularities:
                    for timezone in granularity_timezones:
                        params = {
                            'point': point,
                            'type': energy_type,
                            'activity': activity,
                            'granularity': granularity,
                            'granularitytimezone': timezone,
                            'classification': classification,
                            'validfrom[after]': str(last_week),
                            'validfrom[strictly_before]': str(today)
                        }

                        # API-aanroep
                        response = requests.get(url, headers=headers, params=params)
                        print(f"Status code: {response.status_code}")  # Statuscode check

                        if response.status_code == 200:
                            # Data toevoegen zonder aanpassing
                            data = response.json()
                            if data.get('hydra:totalItems', 0) > 0:
                                all_data.extend(data['hydra:member'])  # Voeg ruwe data toe
                        else:
                            print(f"Fout bij ophalen data: {response.text}")

# Controleer hoeveel data is opgehaald
print(f"Aantal rijen verzameld: {len(all_data)}")

# Exporteer naar Excel
if all_data:
    df = pd.DataFrame(all_data)
    df.to_excel("WindOffshore_RawData.xlsx", index=False)
    print("Data succesvol opgeslagen in WindOffshore_RawData.xlsx")
else:
    print("Geen data om op te slaan.")
