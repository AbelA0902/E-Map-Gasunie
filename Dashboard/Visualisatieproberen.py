import requests
import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Datuminstellingen
start_date = "2022-01-01"  # Begin van de data
today = datetime.date.today()  # Huidige datum

# API URL en headers
url = "https://api.ned.nl/v1/utilizations"
headers = {
    'X-AUTH-TOKEN': '9c99896102ff51d3bf69eca8796b63e2e0a10b9f9e316645e3b80194d041b4a7',
    'accept': 'application/ld+json'
}

# Parameters (pas de waarden aan volgens de handleiding)
params = {
    "startDate": start_date,
    "endDate": today.strftime("%Y-%m-%d"),
    "points": "0, 1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14",  # Verander '14' in een geldige waarde volgens de handleiding
    "types": "18",  # Fossilgaspower
    "activities": "1",  # Providing
    "classifications": "1,2,3",  # Current
    "granularities": "5",  # Per uur
    "granularityTimezones": "1"  # CET
}

# Functie om data op te halen
def fetch_api_data(url, headers, params):
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            print("Data succesvol opgehaald!")
            return response.json()
        else:
            print(f"Fout bij ophalen van data: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Er trad een fout op: {e}")
        return None

# Data ophalen
data = fetch_api_data(url, headers, params)

if data:
    # Controleer de JSON-structuur
    try:
        time_series = [{"time": item["timestamp"], "value": item["value"]} for item in data.get("results", [])]
    except KeyError as e:
        print(f"KeyError: Controleer de structuur van de API-output. Ontbrekende sleutel: {e}")
        time_series = []

    if time_series:
        # Data voorbereiden
        df = pd.DataFrame(time_series)

        # Visualisatie
        plt.figure(figsize=(12, 6))
        plt.plot(df["time"], df["value"], marker="o", linestyle="-", color="b")
        plt.title("Fossil Gas Power Utilization Over Time")
        plt.xlabel("Time")
        plt.ylabel("Utilization")
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.show()
    else:
        print("Geen gegevens gevonden in de API-respons.")
else:
    print("API-aanroep mislukt, controleer je instellingen.")
