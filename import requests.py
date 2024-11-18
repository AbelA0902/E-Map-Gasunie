import requests
import datetime
import pandas as pd

url = "https://api.ned.nl/v1/utilizations"
headers = {'X-AUTH-TOKEN': '7bc33ad38c0e6d7d853994577e34913eec5e26be9a8e13ac6be28ce20b48de22',
           'accept': 'application/ld+json'}

today = datetime.date.today()
last_week = today - datetime.timedelta(days=7) #voor de afgelopen 7 dagen

points = [0, 14]  # Voor heel nederland en offshor
types = [1, 2, 17] #wind ,solar, windoffshore
activities = [1] #providing
classifications = [1, 2, 3] #forecast, current, backcast
granularities = [3, 4, 5, 6] #op welke manier de data is gegroepeerd 10 minuten 15 minuten 1 uur en 1 dag.
granularity_timezones = [0, 1] #alle tijdzones

all_data = []

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

                        response = requests.get(url, headers=headers, params=params)
                        print(f"Status code: {response.status_code}")  # Statuscode check
                        data = response.json()
                        print(data)  # Bekijk de data om te zien of de structuur klopt

                        if data.get('hydra:totalItems', 0) > 0:
                            for item in data['hydra:member']:
                                item['point'] = point
                                item['type'] = energy_type
                                item['activity'] = activity
                                item['classification'] = classification
                                item['granularity'] = granularity
                                item['timezone'] = timezone

                                all_data.append(item)

                            # Controleer de hoeveelheid data
print(f"Aantal rijen verzameld: {len(all_data)}")

# Exporteer naar Excel als er data is
if all_data:
    df = pd.DataFrame(all_data)
    df.to_excel("energy_data.xlsx", index=False)
    print("Data succesvol opgeslagen in energy_data.xlsx")
else:
    print("Geen data om op te slaan.")