import requests
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import json

# Laad het GeoJSON-bestand met de provincies van Nederland
with open('Dashboard\provinces.geojson') as f:
    geojson = json.load(f)

# De API-sleutel en de URL van de API
API_KEY = "9c99896102ff51d3bf69eca8796b63e2e0a10b9f9e316645e3b80194d041b4a7"
API_URL = "https://api.ned.nl/v1/utilizations"

# Stel de headers in voor authenticatie met de API
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Stel de parameters in voor de API-aanroep
params = {
    "Activity": "Providing",  # De activiteit, hier 'Providing' voor opwekking
    "Classification": "Current",  # We willen de actuele data
    "Granularity": 5,  # Hier kiezen we voor 'Hour' granulariteit (5 = Hour)
    "Point": 0,  # Dit is voor Nederland (0 is voor heel Nederland)
    "Type": "1,2,18,17"  # Dit selecteert de energiestromen (Wind, Solar, FossilGasPower, WindOffshore)
}

# Haal de data op uit de API
def get_api_data():
    response = requests.get(API_URL, params=params, headers=headers)

    # Controleer of de request succesvol was (statuscode 200)
    if response.status_code == 200:
        # Haal de JSON data uit de response
        data = response.json()

        # Controleer of we daadwerkelijk data hebben ontvangen
        if data:
            return pd.DataFrame(data)  # Zet de data om in een pandas DataFrame
        else:
            print("Geen data ontvangen van de API.")
            return None
    else:
        # Foutmelding als de request niet succesvol was
        print(f"Fout bij ophalen van data: {response.status_code}")
        print(response.text)
        return None

# Maak een Dash-applicatie aan
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Haal de data op voor gebruik in de app
df = get_api_data()

# Mapping van Point ID naar Provincie naam
province_mapping = {
    1: 'Groningen',
    2: 'Friesland',
    3: 'Drenthe',
    4: 'Overijssel',
    5: 'Flevoland',
    6: 'Gelderland',
    7: 'Utrecht',
    8: 'Noord-Holland',
    9: 'Zuid-Holland',
    10: 'Zeeland',
    11: 'Noord-Brabant',
    12: 'Limburg'
}

# Maak een dictionary om de Point-id's te koppelen aan hun GeoJSON coördinaten
province_geojson_mapping = {}

# Loop door de GeoJSON-gegevens om de provinciecoördinaten te koppelen aan de Point ID's
for feature in geojson['features']:
    properties = feature['properties']
    province_name = properties.get('name')
    # Zoek de bijbehorende Point ID (dit veronderstelt dat de provincie-ID hetzelfde is als in de API)
    for point_id, province in province_mapping.items():
        if province_name == province:
            province_geojson_mapping[point_id] = feature['geometry']

# Layout van het Dashboard
app.layout = html.Div([
    html.H1("Energieverbruik en Opwekking per Provincie in Nederland", style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="province-dropdown",
                options=[{'label': province_mapping[i], 'value': i} for i in province_mapping],
                value=0,
                style={"width": "100%"},
                placeholder="Selecteer een provincie"
            ),
        ], width=4),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='energie-graph')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='province-map')
        ], width=12),
    ])
])

# Callback voor het updaten van de grafiek op basis van de provincie
@app.callback(
    dash.dependencies.Output('energie-graph', 'figure'),
    [dash.dependencies.Input('province-dropdown', 'value')]
)
def update_graph(province_id):
    if df is None:
        return {}
    
    # Filter de data op basis van de geselecteerde provincie
    df_filtered = df[df['Point'] == province_id]

    # Maak een grafiek met Plotly
    fig = px.line(df_filtered, x='timestamp', y='value', color='Type', 
                  title=f"Energieverbruik en Opwekking in Provincie {province_mapping.get(province_id, 'Nederland')}",
                  labels={'timestamp': 'Tijdstip', 'value': 'Opwekking (MWh)'})
    return fig

# Callback voor het updaten van de provinciekaart
@app.callback(
    dash.dependencies.Output('province-map', 'figure'),
    [dash.dependencies.Input('province-dropdown', 'value')]
)
def update_map(province_id):
    if df is None:
        return {}
    
    # Haal de coördinaten van de provincie uit de GeoJSON
    province_geojson = province_geojson_mapping.get(province_id)
    
    if not province_geojson:
        return {}
    
    # Maak een choropleth kaart met de GeoJSON data en Plotly
    fig = px.choropleth(locations=[province_id], 
                        geojson=province_geojson, 
                        color=df[df['Point'] == province_id]['value'], 
                        hover_name='Provincie', 
                        hover_data=["Type", "value"],
                        title="Energieopwekking per Provincie")
    
    # Pas het uiterlijk van de kaart aan
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
