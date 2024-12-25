import requests
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import datetime

# API-configuratie
API_URL = "https://api.ned.nl/v1/utilizations"
headers = {
    'X-AUTH-TOKEN': '9c99896102ff51d3bf69eca8796b63e2e0a10b9f9e316645e3b80194d041b4a7',
    'accept': 'application/ld+json'
}

# Datuminstellingen
start_date = "2022-01-01"  # Begin van de data
today = datetime.date.today()  # Huidige datum

# Parameters die eenvoudig aanpasbaar zijn
point = [0, 14]
types = [18]  # Fossilgaspower
activities = [1]  # Providing
classifications = [1, 2, 3]  # Forecast, Current, Backcast
granularities = [5]  # Per uur
granularity_timezones = [1]  # CET

# Lijst voor het opslaan van alle data
all_data = []

# Itereren over alle parametercombinaties
for points in point:
    for energy_type in types:
        for activity in activities:
            for classification in classifications:
                for granularity in granularities:
                    for timezone in granularity_timezones:
                        params = {
                            'points': points,
                            'types': energy_type,
                            'activities': activity,
                            'classifications': classification,
                            'granularities': granularity,
                            'granularity_timezones': timezone,
                            'start_date': start_date,
                            'end_date': today.strftime('%Y-%m-%d')
                        }
                        response = requests.get(API_URL, params=params, headers=headers)
                        if response.status_code == 200:
                            data = response.json()
                            if data:
                                all_data.extend(data)
                        else:
                            print(f"Fout bij ophalen van data: {response.status_code}")
                            print(response.text)

# Zet de verzamelde data om in een pandas DataFrame
df = pd.DataFrame(all_data)

# Maak een Dash-applicatie aan
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Mapping van Point ID naar Provincie naam en coördinaten
province_mapping = {
    1: {'name': 'Groningen', 'coordinates': (53.2194, 6.5665)},
    2: {'name': 'Friesland', 'coordinates': (53.2012, 5.7999)},
    3: {'name': 'Drenthe', 'coordinates': (52.9925, 6.5642)},
    4: {'name': 'Overijssel', 'coordinates': (52.5168, 6.0830)},
    5: {'name': 'Flevoland', 'coordinates': (52.5185, 5.4714)},
    6: {'name': 'Gelderland', 'coordinates': (51.9851, 5.8987)},
    7: {'name': 'Utrecht', 'coordinates': (52.0907, 5.1214)},
    8: {'name': 'Noord-Holland', 'coordinates': (52.3874, 4.6462)},
    9: {'name': 'Zuid-Holland', 'coordinates': (52.0705, 4.3007)},
    10: {'name': 'Zeeland', 'coordinates': (51.4988, 3.6106)},
    11: {'name': 'Noord-Brabant', 'coordinates': (51.6978, 5.3037)},
    12: {'name': 'Limburg', 'coordinates': (50.8514, 5.6900)}
}

# Voeg coördinaten toe aan de dataframe
if not df.empty:
    df['latitude'] = df['point'].apply(lambda x: province_mapping[x]['coordinates'][0])
    df['longitude'] = df['point'].apply(lambda x: province_mapping[x]['coordinates'][1])

    # Maak een Plotly-figuur
    fig = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        hover_name='point',
        hover_data=['type', 'activity', 'classification'],
        zoom=6,
        height=600
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Voeg de figuur toe aan de Dash-app
    app.layout = html.Div([
        dcc.Graph(id='map', figure=fig)
    ])

if __name__ == '__main__':
    app.run_server(debug=True)