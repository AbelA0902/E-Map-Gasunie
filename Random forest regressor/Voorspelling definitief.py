import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Data inladen vanuit een Excel-bestand
data = pd.read_excel('Opgeschoonde data\cleaned_data_windoffshore.xlsx')

# Converteer 'validfrom' en 'validto' naar datetime
data['validfrom'] = pd.to_datetime(data['validfrom'], errors='coerce')
data['validto'] = pd.to_datetime(data['validto'], errors='coerce')

# Controleer op ontbrekende waarden
if data['validfrom'].isna().any() or data['validto'].isna().any():
    print("Waarschuwing: Sommige datetime-waarden zijn ongeldig. Controleer de data.")
    data = data.dropna(subset=['validfrom', 'validto'])  # Verwijder rijen met ongeldige datums indien nodig

# Maak tijdgerelateerde features
data['hour'] = data['validfrom'].dt.hour
data['day'] = data['validfrom'].dt.day
data['month'] = data['validfrom'].dt.month
data['year'] = data['validfrom'].dt.year

# Selecteer relevante kolommen voor model
features = ['point', 'hour', 'day', 'month', 'year']
X = data[features]  # Let op: 'volume' is hier verwijderd
y = data['volume']  # Gebruik 'volume' alleen als target

# Encodeer categorische kolom 'point'
label_encoder_point = LabelEncoder()
X['point'] = label_encoder_point.fit_transform(X['point'])

# Train een Random Forest-model
model = RandomForestRegressor(random_state=42, n_estimators=100)
model.fit(X, y)

# Maak een toekomstig dataset voor voorspellingen (2025)
points = data['point'].unique()  # Unieke punten uit de data
date_range = pd.date_range(start='2025-01-01', end='2025-12-31 23:59:59', freq='H')  # Elk uur van 2025

# Maak een DataFrame voor alle combinaties van punten en tijdstippen
future_data = pd.DataFrame(
    [(point, dt) for point in points for dt in date_range],
    columns=['point', 'datetime']
)

# Voeg tijdsfeatures toe aan toekomstig dataset
future_data['hour'] = future_data['datetime'].dt.hour
future_data['day'] = future_data['datetime'].dt.day
future_data['month'] = future_data['datetime'].dt.month
future_data['year'] = future_data['datetime'].dt.year

# Verwijder onnodige kolom 'datetime'
future_data = future_data.drop(columns=['datetime'])

# Encodeer 'point' met dezelfde encoder als eerder
future_data['point'] = label_encoder_point.transform(future_data['point'])

# Maak voorspellingen
predictions = model.predict(future_data)

# Voeg voorspellingen toe aan future_data
future_data['predicted_volume'] = predictions

# Exporteer resultaten naar Excel
future_data.to_excel('voorspellingen_2025.xlsx', index=False)

print("Voorspellingen zijn opgeslagen in 'voorspellingen_2025.xlsx'.")
